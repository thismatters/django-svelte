from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from django_svelte_demo.api import views


schema_view = get_schema_view(
    openapi.Info(
        title="svelted API",
        default_version="v1",
        description="Some test endpoints to verify that auth works right",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("requires-auth/", views.RequiresAuthAPIView.as_view(), name="requires-auth"),
    path("public/", views.PublicAPIView.as_view(), name="requires-auth"),
]
