from django.db import models
from django.conf import settings


class PredictionRequest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="predictions"
    )
    label = models.CharField(max_length=255)
    date = models.DateField()
    lat = models.FloatField()
    lon = models.FloatField()

    will_rain = models.BooleanField()
    chance = models.PositiveSmallIntegerField()
    precip_mm = models.FloatField(null=True, blank=True)
    condition = models.CharField(max_length=100, blank=True)

    api_provider = models.CharField(max_length=100, default="WeatherAPI")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.label} @ {self.date} - {'rain' if self.will_rain else 'no rain'}"
