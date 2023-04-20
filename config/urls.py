from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from src.router import routes


# auth/register
urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
# main routes
urlpatterns += [path("admin/", admin.site.urls), path("api/", include(routes))]

urlpatterns += static(settings.VIDEO_URL, document_root=settings.VIDEO_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
