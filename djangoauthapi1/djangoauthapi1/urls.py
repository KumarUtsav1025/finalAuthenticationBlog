from django.contrib import admin
from django.urls import path, include,re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='RoboProject API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('account.urls')),
    path('api/post/', include('roboproject.urls')),
    re_path(r'api/doc/', schema_view)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
