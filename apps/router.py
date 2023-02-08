from django.urls import path, include

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="StaffControl API",
        default_version="v3.1.3",
        description="StaffControl Api implementation",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

routes = [
    path("employees/", include("apps.Employees.urls")),
    path("locations/", include("apps.Locations.urls")),
    path("history/", include("apps.History.urls")),
    path("safety/", include("apps.Safety.urls")),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
