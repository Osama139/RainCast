import json
import urllib.parse
import urllib.request
from django.conf import settings
import datetime

class WeatherApiClient:

    def __init__(self):
        config = settings.APP_CONFIG["weather_api"]
        self.base_url = config["base_url"]
        self.api_key = config["key"]

    def search_locations(self, query: str, limit: int = 5):
        if not query or not query.strip():
            return []

        endpoint = f"{self.base_url}/search.json"
        params = urllib.parse.urlencode({"key": self.api_key, "q": query})
        url = f"{endpoint}?{params}"

        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.load(response)

        results = []
        for result in data[:limit]:
            results.append({
                "name": result["name"],
                "region": result["region"],
                "country": result["country"],
                "lat": result["lat"],
                "lon": result["lon"],
            })
        return results

    def get_daily_forecast(self, lat: float, lon: float, target_date: datetime.date):
        today = datetime.date.today()
        delta_days = (target_date - today).days
        if delta_days < 0:
            raise ValueError("Target date must be later than today")

        days = min(14, delta_days + 1)
        q = f"{lat},{lon}"
        endpoint = f"{self.base_url}/forecast.json"
        params = urllib.parse.urlencode(
            {
                "key": self.api_key,
                "q": q,
                "days": days,
                "aqi": "no",
                "alerts": "no"
            }
        )
        url = f"{endpoint}?{params}"

        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.load(response)

        for item in (data.get("forecast", {}) or {}).get("forecastday", []):
            if item.get("date") == target_date.isoformat():
                day = item.get("day", {}) or {}
                chance = day.get("daily_chance_of_rain")
                daily_will = day.get("daily_will_it_rain")
                try:
                    chance = int(chance) if chance else 0
                except (TypeError, ValueError):
                    chance = 0
                will = bool(int(daily_will)) if daily_will else (chance >= 50)
                return {
                    "date": item.get("date"),
                    "chance": chance,
                    "will_rain": will,
                    "pop": chance/100.0,
                    "precip_mm": day.get("totalprecip_mm"),
                    "condition": (day.get("condition") or {}).get("text"),
                }

        raise Exception("No forecast for this date")

