from typing import Any

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from models_api.models import AIModel, ModelAuthor
from models_api.serializers import (
    AIModelSerializer,
    ModelAuthorSerializer,
    ModelBenchmarkSerializer,
    UsageScenarioSerializer,
)


class ModelAuthorViewSet(viewsets.ModelViewSet):
    queryset = ModelAuthor.objects.all()
    serializer_class = ModelAuthorSerializer

    @action(detail=True, methods=["get"])
    def models(self, _request: Request, **kwargs: Any) -> Response:
        author = self.get_object()
        models = author.models_uploaded.all()
        serializer = AIModelSerializer(models, many=True)

        return Response(serializer.data)


class AIModelViewSet(viewsets.ModelViewSet):
    queryset = AIModel.objects.all()
    serializer_class = AIModelSerializer

    @action(detail=True, methods=["get"])
    def usage_scenarios(self, _request: Request, **kwargs: Any) -> Response:
        model = self.get_object()
        scenarios = model.usage_scenarios.all()
        serializer = UsageScenarioSerializer(scenarios, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def benchmarks(self, _request: Request, **kwargs: Any) -> Response:
        model = self.get_object()
        benchmarks = model.benchmarks.all()
        serializer = ModelBenchmarkSerializer(benchmarks, many=True)

        return Response(serializer.data)
