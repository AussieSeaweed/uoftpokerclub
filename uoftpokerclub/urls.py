"""uoftpokerclub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views import generic
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path("community/", include("community.urls")),
    path("gamemaster/", include("gamemaster.urls")),
    path("blog/", include("blog.urls")),

    path("", generic.TemplateView.as_view(template_name="uoftpokerclub/home.html"), name="home"),
]

if settings.DEBUG:
    urlpatterns.append(path(f"{settings.MEDIA_URL[1:]}<path:path>", serve, {'document_root': settings.MEDIA_ROOT}))
