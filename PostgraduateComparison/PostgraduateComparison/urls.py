
from django.contrib import admin
from django.urls import path, include
from application.admin import post_admin_site
from django.conf import settings
from django.conf.urls.static import static
# from application.admin import blog_admin
urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_site/', post_admin_site.urls),
    path('', include('application.urls')),
    path('account/', include('accounts.api.urls')),
    path('api-auth/', include("rest_framework.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
