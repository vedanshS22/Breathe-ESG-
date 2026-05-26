from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from api.views.frontend_views import AnalystAppView


urlpatterns = [
    path("", AnalystAppView.as_view(), name="analyst-app"),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    re_path(r"^(?:dashboard|upload|review|audit)/?$", AnalystAppView.as_view(), name="react-routes"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
