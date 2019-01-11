from _weakrefset import WeakSet
from functools import update_wrapper

from django.apps import apps
from django.contrib.auth import REDIRECT_FIELD_NAME, logout
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from django.db.models.base import ModelBase
from django.http import HttpResponseRedirect, Http404
from django.template.response import TemplateResponse
from django.urls import reverse, re_path
from django.utils.functional import LazyObject
from django.utils.module_loading import import_string
from django.utils.text import capfirst
from django.utils.translation import gettext as _, gettext_lazy
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from app_client.options import ModelClient

all_sites = WeakSet()


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class AppClientSite:
    # Text to put at the end of each page's <title>.
    site_title = gettext_lazy('Application Client')

    # Text to put in each page's <h1>.
    site_header = gettext_lazy('Application Client')

    # Text to put at the top of the client index page.
    index_title = gettext_lazy('Application Client')

    # URL for the "View site" link at the top of each client page.
    site_url = '/'

    _empty_value_display = '-'

    index_template = None
    app_index_template = None

    def __init__(self, name='client'):
        self._registry = {}
        self.name = name
        all_sites.add(self)

    def register(self, model_or_iterable, client_class=None, **options):
        client_class = client_class or ModelClient
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model._meta.abstract:
                raise ImproperlyConfigured(
                    'The model %s is abstract, so it cannot be registered with client.' % model.__name__
                )
            if model in self._registry:
                raise AlreadyRegistered('The model %s is already registered' % model.__name__)

            # Ignore the registration if the model has been
            # swapped out.
            if not model._meta.swapped:
                # If we got **options then dynamically construct a subclass of
                # client_class with those **options.
                if options:
                    options['__module__'] = __name__
                    client_class = type("%sClient" % model.__name__, (client_class,), options)

                # Instantiate the client class to save in the registry
                self._registry[model] = client_class(model, self)

    def unregister(self, model_or_iterable):
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model not in self._registry:
                raise NotRegistered('The model %s is not registered' % model.__name__)
            del self._registry[model]

    def is_registered(self, model):
        return model in self._registry

    def has_permission(self, request):
        return request.user.is_active and request.user.is_staff

    def client_view(self, view, cacheable=False):
        from django.conf import settings
        def go_to_login(request):
            if request.path == reverse('logout', current_app=self.name):
                index_path = reverse('client:index', current_app=self.name)
                return HttpResponseRedirect(index_path)
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                request.get_full_path(),
                reverse('login' or settings.LOGIN_URL, current_app=self.name),
                REDIRECT_FIELD_NAME
            )

        def validate_login_session(request):
            from app_authentication.config import USER_SESSION_CACHE_KEY
            if request.user and str(request.user) != 'AnonymousUser':
                session_key = cache.get(USER_SESSION_CACHE_KEY % request.user.id, request.session.session_key)
                if session_key != request.session.session_key:
                    logout(request)
                    return False
            return True

        def inner(request, *args, **kwargs):
            from main.views import BaseView
            if hasattr(view, 'view_class') and issubclass(view.view_class, BaseView):
                view_class = view.view_class
                if view_class.login_required or view_class.admin_required or view_class.superuser_required:
                    user = request.user
                    if user is None or not user.is_authenticated or not user.is_active or (
                                    request.user.is_active and not settings.LOGIN_MULTI_LOCATION and not validate_login_session(request)):
                        return go_to_login(request)
                    if view_class.superuser_required and not request.user.is_superuser:
                        return view.go_to_login()
                    if view_class.admin_required and not request.user.is_admin:
                        return go_to_login(request)

                app_list = self.get_app_list(request)
                view_class.more_context = {
                    **self.each_context(request),
                    'title': self.index_title,
                    'app_list': app_list,
                    'current_app': self.name
                }

            else:
                if not self.has_permission(request):
                    return go_to_login(request)

            return view(request, *args, **kwargs)

        if not cacheable:
            inner = never_cache(inner)
        # We add csrf_protect here so this function can be used as a utility
        # function for any view, without having to repeat 'csrf_protect'.
        if not getattr(view, 'csrf_exempt', False):
            inner = csrf_protect(inner)
        return update_wrapper(inner, view)

    def get_urls(self):
        from django.urls import include, path
        # Since this module gets imported in the application's root package,
        # it cannot import models from other applications at the module level,
        # and django.contrib.contenttypes.views imports ContentType.

        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.client_view(view, cacheable)(*args, **kwargs)

            wrapper.client_site = self
            return update_wrapper(wrapper, view)

        # Client-site-wide views.
        from app_client.views import Index
        urlpatterns = [
            path('', wrap(Index.as_view()), name='index'),
        ]

        # Add in each model's views, and create a list of valid URLS for the
        # app_index
        valid_app_labels = []
        for model, model_client in self._registry.items():
            if model_client.urls:
                urlpatterns += [
                    path('%s/' % model._meta.app_url_prefix, include(model_client.urls)),
                ]
                if model._meta.app_label not in valid_app_labels:
                    valid_app_labels.append(model._meta.app_label)
        if valid_app_labels:
            regex = r'^(?P<app_label>' + '|'.join(valid_app_labels) + ')/$'
            urlpatterns += [
                re_path(regex, wrap(self.app_index), name='app_list'),
            ]
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'client', self.name

    def each_context(self, request):
        """
        Return a dictionary of variables to put in the template context for
        *every* page in the client site.

        For sites running on a subpath, use the SCRIPT_NAME value if site_url
        hasn't been customized.
        """
        script_name = request.META['SCRIPT_NAME']
        site_url = script_name if self.site_url == '/' and script_name else self.site_url
        return {
            'site_title': self.site_title,
            'site_header': self.site_header,
            'site_url': site_url,
            'available_apps': self.get_app_list(request),
        }

    def _build_app_dict(self, request, label=None):
        """
        Build the app dictionary. The optional `label` parameter filters models
        of a specific app.
        """
        app_dict = {}

        if label:
            models = {
                m: m_a for m, m_a in self._registry.items()
                if m._meta.app_label == label
            }
        else:
            models = self._registry

        for model, model_client in models.items():
            app_label = model._meta.app_label

            # has_module_perms = model_client.has_module_permission(request)
            # if not has_module_perms:
            #     continue
            #
            # perms = model_client.get_model_perms(request)
            #
            # # Check whether user has any perm for this module.
            # # If so, add the module to the model_list.
            # if True not in perms.values():
            #     continue

            info = (app_label, model._meta.model_name)
            model_dict = {
                'name': capfirst(model._meta.verbose_name_plural),
                'object_name': model._meta.object_name,
                'perms': {},
            }
            # if perms.get('change') or perms.get('view'):
            #     model_dict['view_only'] = not perms.get('change')
            #     try:
            #         model_dict['client_url'] = reverse('client:%s_%s_changelist' % info, current_app=self.name)
            #     except NoReverseMatch:
            #         pass
            # if perms.get('add'):
            #     try:
            #         model_dict['add_url'] = reverse('client:%s_%s_add' % info, current_app=self.name)
            #     except NoReverseMatch:
            #         pass

            if app_label in app_dict:
                app_dict[app_label]['models'].append(model_dict)
            else:
                app_dict[app_label] = {
                    'name': apps.get_app_config(app_label).verbose_name,
                    'app_label': app_label,
                    'app_url': reverse(
                        'client:app_list',
                        kwargs={'app_label': app_label},
                        current_app=self.name,
                    ),
                    'has_module_perms': True,
                    'models': [model_dict],
                }

        if label:
            return app_dict.get(label)
        return app_dict

    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request)

        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'])

        return app_list

    def app_index(self, request, app_label, extra_context=None):
        app_dict = self._build_app_dict(request, app_label)
        if not app_dict:
            raise Http404('The requested client page does not exist.')
        # Sort the models alphabetically within each app.
        app_dict['models'].sort(key=lambda x: x['name'])
        app_name = apps.get_app_config(app_label).verbose_name
        context = {
            **self.each_context(request),
            'title': _('%(app)s client') % {'app': app_name},
            'app_list': [app_dict],
            'app_label': app_label,
            **(extra_context or {}),
        }

        request.current_app = self.name

        return TemplateResponse(request, self.app_index_template or [
            'app_modules/%s/templates/%s/index.html' % app_label,
            'app_client/index.html'
        ], context)


class DefaultAppClientSite(LazyObject):
    def _setup(self):
        AppClientSiteClass = import_string(apps.get_app_config('app_client').default_site)
        self._wrapped = AppClientSiteClass()


site = DefaultAppClientSite()
