from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import index

urlpatterns = [
    path("api/v1/", include("crm.urls")),
    # path("test/", include("mis.urls")),
    # path("tasks/", include("tasks.urls")),
    # path("", admin.site.urls, name="admin"),
    path("", index),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
