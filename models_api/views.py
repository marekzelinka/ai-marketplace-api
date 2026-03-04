from typing import Any

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from models_api.models import ModelAuthor
from models_api.serializers import AIModelSerializer, ModelAuthorSerializer


class ModelAuthorViewSet(viewsets.ModelViewSet):
    queryset = ModelAuthor.objects.all()
    serializer_class = ModelAuthorSerializer

    @action(detail=True, methods=["get"])
    def models(self, _request: Request, **kwargs: Any) -> Response:
        author = self.get_object()
        models = author.models_uploaded.all()
        serializer = AIModelSerializer(models, many=True)

        return Response(serializer.data)
