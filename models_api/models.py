from typing import Any

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class ModelAuthor(models.Model):
    """Represents the creator of AI models."""

    class Meta:
        indexes = [models.Index(fields=["name"]), models.Index(fields=["rating"])]

    id: int
    name = models.CharField(max_length=200)
    bio = models.TextField()
    contact_info = models.EmailField(unique=True)
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    models_uploaded: models.BaseManager[AIModel]

    def __str__(self) -> str:
        return self.name


class AIModel(models.Model):
    """Represents individual AI models with their details."""

    class Meta:
        # Default ordering: newest first, then by name
        ordering = ["-id", "name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["framework", "model_type"]),
        ]
        constraints = [
            # Prevents uploading the same version of a model twice
            models.UniqueConstraint(
                fields=["name", "version"],
                name="%(app_label)s_%(class)s_unique_model_version",
            ),
            models.CheckConstraint(
                condition=models.Q(price__gte=0),
                name="%(app_label)s_%(class)s_price_not_negative",
            ),
        ]

    MODEL_TYPES = [
        ("NLP", "Natural Language Processing"),
        ("CV", "Computer Vision"),
        ("RL", "Reinforcment Learning"),
        ("OTHER", "Other"),
    ]
    FRAMEWORKS = [
        ("PT", "PyTorch"),
        ("TF", "TensorFlow"),
        ("KRS", "Keras"),
        ("OTHER", "Other"),
    ]

    id: int
    name = models.CharField(max_length=200)
    model_type = models.CharField(max_length=5, choices=MODEL_TYPES)
    description = models.TextField()
    framework = models.CharField(max_length=5, choices=FRAMEWORKS)
    version = models.CharField(max_length=50)
    download_url = models.URLField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    tags = (
        models.JSONField()
    )  # TODO: refactor to tag model and aimodel-tags-link (many-to-many)

    author_id: int
    author = models.ForeignKey(
        ModelAuthor,
        on_delete=models.CASCADE,
        related_name="models_uploaded",
    )

    purchases: models.BaseManager[ModelPurchase]
    usage_scenarios: models.BaseManager[UsageScenario]
    benchmarks: models.BaseManager[ModelBenchmark]

    def __str__(self) -> str:
        return f"{self.name} - {self.version}"


class ModelPurchase(models.Model):
    """Tracks purchases and downloads of AI models."""

    class Meta:
        indexes = [models.Index(fields=["purchase_date"])]
        get_latest_by = "purchase_date"

    id: int
    user = models.CharField(
        max_length=200
    )  # TODO: setup username/password auth with drf
    purchase_date = models.DateTimeField(auto_now_add=True)
    price_paid = models.DecimalField(max_digits=10, decimal_places=2)
    license_key = models.CharField(max_length=100)
    download_link = models.URLField()

    ai_model_id: int
    ai_model = models.ForeignKey(
        AIModel, on_delete=models.CASCADE, related_name="purchases"
    )

    def clean(self) -> None:
        """Cross-field validation: ensure price_paid doesn't exceed listed price."""
        if self.price_paid > self.ai_model.price:
            raise ValidationError(
                {"price_paid": "Price paid cannot exceed the listed model price."},
                code="invalid",
            )

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Enforce validation on every save, including programmatic ones."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user} - {self.ai_model.name}"


class UsageScenario(models.Model):
    """Represents suggested use cases for each AI model."""

    id: int
    title = models.CharField(max_length=200)
    description = models.TextField()
    code_snippet = models.TextField()
    usage_frequency = models.IntegerField(default=0)

    ai_model_id: int
    ai_model = models.ForeignKey(
        AIModel, on_delete=models.CASCADE, related_name="usage_scenarios"
    )

    def __str__(self) -> str:
        return f"{self.ai_model.name} - {self.title}"


class ModelBenchmark(models.Model):
    """Stores performance benchmarks for AI models."""

    id: int
    metric_name = models.CharField(max_length=100)
    value = models.FloatField()
    benchmark_date = models.DateTimeField(auto_now_add=True)
    hardware_used = models.CharField(max_length=200)

    ai_model_id: int
    ai_model = models.ForeignKey(
        AIModel, on_delete=models.CASCADE, related_name="benchmarks"
    )

    def __str__(self) -> str:
        return f"{self.ai_model.name} - {self.metric_name}: {self.value}"
