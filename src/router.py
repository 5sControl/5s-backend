from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework import permissions

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
    path("staff-control/", include("src.StaffControl.staffcontrol_router")),
    path("cameras/", include("src.Cameras.urls")),
    path("algorithms/", include("src.Algorithms.urls")),
    path("reports/", include("src.Reports.urls")),
    path("company/", include("src.CompanyLicense.urls")),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
