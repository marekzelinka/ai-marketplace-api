from django.urls import include, path
from rest_framework.routers import DefaultRouter

from models_api.views import (
    AIModelViewSet,
    ModelAuthorViewSet,
    ModelBenchmarkViewSet,
    ModelPurchaseViewSet,
    UsageScenarioViewSet,
)

router = DefaultRouter()
router.register(r"authors", ModelAuthorViewSet)
router.register(r"models", AIModelViewSet)
router.register(r"purchases", ModelPurchaseViewSet)
router.register(r"usage-scenarios", UsageScenarioViewSet)
router.register(r"benchmarks", ModelBenchmarkViewSet)

urlpatterns = [path("", include(router.urls))]
