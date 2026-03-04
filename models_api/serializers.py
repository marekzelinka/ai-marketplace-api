from rest_framework import serializers

from models_api.models import (
    AIModel,
    ModelAuthor,
    ModelBenchmark,
    ModelPurchase,
    UsageScenario,
)


class ModelAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelAuthor
        fields = ["id", "name", "bio", "contact_info", "rating"]


class AIModelSerializer(serializers.ModelSerializer):
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=ModelAuthor.objects.all(), source="author", write_only=True
    )
    author = ModelAuthorSerializer(read_only=True)

    class Meta:
        model = AIModel
        fields = [
            "id",
            "name",
            "model_type",
            "description",
            "framework",
            "version",
            "download_url",
            "price",
            "tags",
            "author",
            "author_id",
        ]


class ModelPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelPurchase
        fields = [
            "id",
            "user",
            "ai_model",
            "purchase_date",
            "price_paid",
            "license_key",
            "download_link",
        ]


class UsageScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsageScenario
        field = [
            "id",
            "ai_model",
            "title",
            "description",
            "code_snippet",
            "usage_frequency",
        ]


class ModelBenchmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelBenchmark
        fields = [
            "id",
            "ai_model",
            "metric_name",
            "value",
            "benchmark_date",
            "hardware_used",
        ]
