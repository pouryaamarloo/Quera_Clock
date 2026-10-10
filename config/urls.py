from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from config.settings.base import MEDIA_ROOT,MEDIA_URL

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include("apps.workspaces.urls", namespace="workspaces")),
    path("auth/",include("apps.users.urls", namespace="users")),
    # COURSE_TODO: add the admin route.
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=MEDIA_ROOT)