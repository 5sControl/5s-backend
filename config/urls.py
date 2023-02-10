from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from apps.router import routes
from .views import RegisterView, GetIp, setcookie, getcookie


urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("get_ip/", GetIp.as_view()),
    path("api-auth/", include("rest_framework.urls")),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("admin/", admin.site.urls),
    path("api/", include(routes)),
]
urlpatterns += [
    path("scookie", setcookie),
    path("gcookie", getcookie),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
