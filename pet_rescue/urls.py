from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from pets.api_views import AdoptionRequestViewSet, PetViewSet

router = DefaultRouter()
router.register('pets', PetViewSet, basename='api-pets')
router.register('adoptions', AdoptionRequestViewSet, basename='api-adoptions')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pets.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include(router.urls)),
    path('api/token/', obtain_auth_token, name='api-token'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
