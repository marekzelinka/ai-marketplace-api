from django.urls import include, path
from rest_framework.routers import DefaultRouter

from models_api.views import AIModelViewSet, ModelAuthorViewSet

router = DefaultRouter()
router.register(r"authors", ModelAuthorViewSet)
router.register(r"models", AIModelViewSet)

urlpatterns = [path("", include(router.urls))]
