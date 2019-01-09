from django.conf import settings
from django.http import HttpResponseRedirect


def secure_required(func):
    """
    Decorator makes sure URL is accessed over https.
    Use with `SecureRequiredMiddleware` to ensure only decorated urls are
    accessed via https
    """

    def wrap(request, *args, **kwargs):
        request.META["CSRF_COOKIE_USED"] = True
        request.secure_required = True
        if not request.is_secure():
            if getattr(settings, 'HTTPS_SUPPORT', False):
                request_url = request.build_absolute_uri(request.get_full_path())
                secure_url = request_url.replace('http://', 'https://')
                return HttpResponseRedirect(secure_url)
        return func(request, *args, **kwargs)

    return wrap