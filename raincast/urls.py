from django.urls import path
from .views import HomeView, PredictionView, LocationSearchApiView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("prediction/", PredictionView.as_view(), name="prediction"),
    path('api/search_location/', LocationSearchApiView.as_view(), name="api_search_location"),
]