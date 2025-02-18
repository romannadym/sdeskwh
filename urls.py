"""integrator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from integrator.apps.api_services import *

urlpatterns = [
    path('', include('main.urls')),
    path('', include('login.urls')),
    path('applications/', include('applications.urls')),
    path('equipments/', include('equipments.urls')),
    path('spares/', include('spares.urls')),
    path('contracts/', include('contracts.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', include('admin.urls')),
    path('articles/', include('articles.urls')),
    path("select2/", include("django_select2.urls")),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    path('api/engineers/', EngineersListAPIView.as_view()),
    # path('admin/', admin.site.urls),
    # url(r'^_nested_admin/', include('nested_admin.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
