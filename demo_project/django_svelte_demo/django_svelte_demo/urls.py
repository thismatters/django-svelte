"""django_svelte_demo URL Configuration

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
from django.contrib import admin
from django.urls import path, include

from django.views.generic import TemplateView

from .views import MySvelteTemplateView, MyContextSvelteTemplateView

urlpatterns = [
    path(
        "",
        TemplateView.as_view(
            template_name="basic.html",
            extra_context={"component_props": {"name": "django-svelte"}},
        ),
        name="home",
    ),
    path(
        "single/main/",
        MyContextSvelteTemplateView.as_view(
            page_title="Main Component", component_name="App"
        ),
        name="main-component",
    ),
    path(
        "single/auth/",
        MySvelteTemplateView.as_view(
            page_title="Auth Component", component_name="AuthComponent"
        ),
        name="auth-component",
    ),
    path(
        "single/post/",
        MySvelteTemplateView.as_view(
            page_title="Post Component", component_name="PostComponent"
        ),
        name="post-component",
    ),
    path("admin/", admin.site.urls),
    path("api/v1/", include("django_svelte_demo.api.urls")),
]
