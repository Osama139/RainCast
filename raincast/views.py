from django.http import JsonResponse
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from raincast.forms import PredictionForm
from raincast.integrations.weather_api_client import WeatherApiClient
from raincast.models import PredictionRequest


class HomeView(TemplateView):
    template_name = "raincast/home.html"


class PredictionView(LoginRequiredMixin, FormView):
    template_name = "raincast/prediction.html"
    form_class = PredictionForm

    def form_valid(self, form):
        cleaned = form.cleaned_data
        location_label = cleaned["location"]
        lat = cleaned.get("lat")
        lon = cleaned.get("lon")
        client = WeatherApiClient()

        if not (lat and lon):
            matches = client.search_locations(location_label, limit=1)
            if not matches:
                form.add_error("location", f"Could not find location {location_label}. Please choose from suggestions")
                return self.form_invalid(form)
            lat = matches[0].get("lat")
            lon = matches[0].get("lon")
            parts = [matches[0].get("name"), matches[0].get("region"), matches[0].get("country")]
            location_label = ", ".join([p for p in parts if p])

        try:
            forecast = client.get_daily_forecast(float(lat), float(lon), cleaned["date_"])
        except Exception as e:
            form.add_error(None, f"Could not fetch forecast for {location_label}. {e}")
            return self.form_invalid(form)

        label = location_label or cleaned["location"]
        PredictionRequest.objects.create(
            user = self.request.user,
            label = label,
            date = cleaned["date_"],
            lat = float(lat),
            lon = float(lon),
            will_rain=forecast["will_rain"],
            chance=int(forecast["chance"]),
            precip_mm=forecast.get("precip_mm"),
            condition=forecast.get("condition") or "",
            api_provider="WeatherAPI",
        )
        condition = (forecast.get("condition") or "").lower()
        rain_kw = ("rain", "drizzle", "shower", "storm", "thunder")
        cloud_kw = ("cloud", "overcast", "mist", "fog", "haze", "smoke")

        if forecast.get("will_rain") or any(k in condition for k in rain_kw):
            bg_class = "bg-rainy"
        elif any(k in condition for k in cloud_kw):
            bg_class = "bg-cloudy"
        else:
            bg_class = "bg-sunny"
        context = self.get_context_data(form=form)
        context.update({
            "submitted": True,
            "cleaned": cleaned,
            "resolved_label": location_label,
            "forecast": forecast,
            "bg_class": bg_class,
        })
        return self.render_to_response(context)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class LocationSearchApiView(LoginRequiredMixin, View):

    def get(self, request):
        q = (request.GET.get("q") or "").strip()
        client = WeatherApiClient()
        results = client.search_locations(q, limit=10)
        return JsonResponse(results, safe=False)