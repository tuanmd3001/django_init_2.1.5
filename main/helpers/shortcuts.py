"""
This module collects helper functions and classes that "span" multiple levels
of MVC. In other words, these functions/classes introduce controlled coupling
for convenience's sake.
"""
import os
import warnings

from constance import config
from django.http import (
    HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect,
)
from django.shortcuts import resolve_url
from django.template import loader
from django.utils.deprecation import RemovedInDjango30Warning


def template_render_to_response(template_name, context=None, content_type=None, status=None, using=None):
    """
    Return a HttpResponse whose content is filled with the result of calling
    django.template.loader.render_to_string() with the passed arguments.
    """
    warnings.warn(
        'render_to_response() is deprecated in favor of render(). It has the '
        'same signature except that it also requires a request.',
        RemovedInDjango30Warning, stacklevel=2,
    )
    content = loader.render_to_string(os.path.join(config.THEME, config.THEME_TEMPLATE_DIR, template_name), context, using=using)
    return HttpResponse(content, content_type, status)


def template_render(request, template_name, context=None, content_type=None, status=None, using=None):
    """
    Return a HttpResponse whose content is filled with the result of calling
    django.template.loader.render_to_string() with the passed arguments.
    """
    content = loader.render_to_string(os.path.join(config.THEME, config.THEME_TEMPLATE_DIR, template_name), context, request, using=using)
    return HttpResponse(content, content_type, status)


def template_redirect(to, *args, permanent=False, **kwargs):
    """
    Return an HttpResponseRedirect to the appropriate URL for the arguments
    passed.

    The arguments could be:

        * A model: the model's `get_absolute_url()` function will be called.

        * A view name, possibly with arguments: `urls.reverse()` will be used
          to reverse-resolve the name.

        * A URL, which will be used as-is for the redirect location.

    Issues a temporary redirect by default; pass permanent=True to issue a
    permanent redirect.
    """
    redirect_class = HttpResponsePermanentRedirect if permanent else HttpResponseRedirect
    return redirect_class(resolve_url(to, *args, **kwargs))
