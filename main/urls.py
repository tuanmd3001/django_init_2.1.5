"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from importlib import import_module
from django.contrib import admin
from django.urls import path, include

# from django.conf import settings
# from django.conf.urls.static import static
from main import settings

urlpatterns = [
    path('admin_base/', admin.site.urls),
]
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


for app in settings.INSTALLED_APPS:
    try:
        mod = import_module('%s.urls' % app)
        # possibly cleanup the after the imported module?
        #  might fuss up the `include(...)` or leave a polluted namespace
    except:
        # cleanup after module import if fails,
        #  maybe you can let the `include(...)` report failures
        pass
    else:
        urlpatterns.append(path('', include('%s.urls' % app)))
