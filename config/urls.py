from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include

from src.router import routes

urlpatterns = [

    path("api/", include(routes)),
]

urlpatterns += static(settings.VIDEO_URL, document_root=settings.VIDEO_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
