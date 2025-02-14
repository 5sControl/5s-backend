from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework import permissions

from rest_framework_simplejwt.authentication import JWTAuthentication

routes = [
    path("api-auth/", include("rest_framework.urls")),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),

    path("employees/", include("src.Employees.urls"), name="employees"),
    path("camera-algorithms/", include("src.CameraAlgorithms.urls"), name="camera-algorithms"),
    path("reports/", include("src.Reports.urls"), name="reports"),
    path("company/", include("src.CompanyLicense.urls"), name="company"),
    path("order/", include("src.OrderView.urls"), name="order"),
    path("new-order/", include("src.newOrderView.urls"), name="new-order"),
    path("inventory/", include("src.Inventory.urls"), name="inventory"),
    path("mailer/", include("src.Mailer.urls"), name="mailer"),
    path("core/", include("src.Core.urls"), name="core"),
    path("suppliers/", include("src.Suppliers.urls"), name="suppliers"),
    path("connector/", include("src.DatabaseConnections.urls"), name="connector"),
    path("healthcheck/", include("src.Healthcheck.urls"), name="healthcheck"),
    path("erp-reference/", include("src.references.urls"), name="reference-erp"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


schema_view = get_schema_view(
    openapi.Info(
        title="5controlS API",
        default_version="v3.1.3",
        description="5controlS Api implementation",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[JWTAuthentication],
    patterns=[path("api/", include(routes))],
    urlconf='config.urls',
)

routes += [
    path(
        "swagger/",
        schema_view.with_ui("swagger"),
        name="schema-swagger-ui",
    ),
]
