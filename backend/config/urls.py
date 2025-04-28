
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from applications.cert.views import CertViewSet

router = DefaultRouter()
router.register(r'', CertViewSet, basename='cert')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/cert/', include(router.urls)),
    path('api/v1/token/',TokenRefreshView.as_view(),name="token_refresh")
]
