import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from raincast.models import PredictionRequest
from raincast.integrations import weather_api_client as weather_mod

@pytest.mark.django_db
def test_homepage_renders(client):
    r = client.get(reverse("home"))
    assert r.status_code == 200

@pytest.mark.django_db
def test_prediction_requires_login(client):
    r = client.get(reverse("prediction"))
    assert r.status_code == 302
    assert "login" in r.url

@pytest.mark.django_db
def test_prediction_page_renders_for_authenticated_user(client):
    user = User.objects.create_user(username="testuser", password="TestUser123!")
    client.login(username="testuser", password="TestUser123!")
    r = client.get(reverse("prediction"))
    assert r.status_code == 200
    assert b"Prediction" in r.content

@pytest.mark.django_db
def test_prediction_post_creates_row_and_shows_result(client, monkeypatch):
    # login
    user = User.objects.create_user(username="testuser", password="StrongPass123!")
    client.login(username="testuser", password="StrongPass123!")

    # mock forecast
    monkeypatch.setattr(
        weather_mod.WeatherApiClient,
        "get_daily_forecast",
        lambda self, lat, lon, target_date: {
            "date": target_date.isoformat(),
            "chance": 70,
            "will_rain": True,
            "precip_mm": 5.0,
            "condition": "Light rain",
        },
    )

    resp = client.post(reverse("prediction"), data={
        "location": "Karachi, Sindh, Pakistan",
        "date_": date.today().isoformat(),
        "lat": "24.86",
        "lon": "67.01",
    })

    assert resp.status_code == 200
    assert b"chance of rain" in resp.content

    assert PredictionRequest.objects.count() == 1