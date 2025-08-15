from django.contrib import admin
from raincast.models import PredictionRequest


@admin.register(PredictionRequest)
class PredictionRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "label", "date", "will_rain", "chance", "created_at")
    list_filter = ("will_rain", "date", "created_at")
    search_fields = ("label", "user__username")