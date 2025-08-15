# RainCast

A Django app that lets users sign up, log in, search for locations, and check “will it rain?” for a chosen date, using an open weather API.  
All users are stored in **PostgreSQL**, DB credentials (for local dev) live in **`conf/app_config.json`**, and each prediction is saved in a separate table per user; per the task spec.  

---

## Contents
- [Quickstart](#quickstart)
- [Configuration (`conf/app_config.json`)](#configuration-conf_app_configjson)
- [Running](#running)
- [Endpoints & JSON I/O](#endpoints--json-io)
- [Tests](#tests)



## Quickstart

```bash
# 1) clone and enter the project
git clone <your-repo-url>.git
cd RainCast

# 2) create and activate a virtualenv
python -m venv venv
source venv/bin/activate

# 3) install dependencies
pip install -r requirements.txt

# 4) configure PostgreSQL matching conf/app_config.json (below)
#    create role & DB locally (example):
#    sudo -u postgres psql -c "CREATE ROLE raincast_user LOGIN PASSWORD 'raincast123';"
#    sudo -u postgres psql -c "ALTER ROLE raincast_user CREATEDB;"
#    sudo -u postgres createdb -O raincast_user raincast

# 5) migrations
python manage.py migrate

# 6) (optional) create a superuser
python manage.py createsuperuser

# 7) run
python manage.py runserver
```

## Configuration (`conf/app_config.json`)

All local dev config lives in `conf/app_config.json`. The app **loads this file first**, then applies any **environment variable overrides** (useful for CI).

**Example**
```json
{
  "database": {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": "raincast",
    "USER": "raincast_user",
    "PASSWORD": "raincast123",
    "HOST": "localhost",
    "PORT": 5432
  },
  "weather_api": {
    "base_url": "http://api.weatherapi.com/v1",
    "key": "YOUR_WEATHER_API_KEY"
  }
}
```

## Running

Start the dev server:
```bash
python manage.py runserver
```

Endpoints (local)

Home: /

Sign Up: /accounts/signup/

Login: /accounts/login/

Prediction (auth): GET, POST /prediction/

Location Search API (JSON): /api/search_location/?q=<text>


## Endpoints & JSON I/O

> Base URL (dev): `http://127.0.0.1:8000`

---

### 1) Location Search — `GET /api/search_location/?q=<text>`

**Input (query)**
```json
{ "q": "Lon" }

curl http://127.0.0.1:8000/api/search_location/?q=Lon

Response (200 JSON):

[
  {
    "name": "London",
    "region": "City of London, Greater London",
    "country": "United Kingdom",
    "lat": 51.52,
    "lon": -0.11
  },
  {
    "name": "London",
    "region": "Ontario",
    "country": "Canada",
    "lat": 42.98,
    "lon": -81.25
  }
]
```
### 2) Prediction (HTML page) — `GET/POST /prediction/ (login required)`

**Input (query)**
```json
{
  "location": "Karachi, Sindh, Pakistan",
  "date_": "2025-08-20",
  "lat": 24.86,
  "lon": 67.01
}

curl http://api.weatherapi.com/v1/forecast.json?key=$API_KEY&q=24.86,67.01&days=6&aqi=no&alerts=no

Response (200 JSON):

[
  {
  "date": "2025-08-20",
  "day": {
    "maxtemp_c": 34.5,
    "mintemp_c": 28.1,
    "avgtemp_c": 31.2,
    "daily_chance_of_rain": 70,
    "totalprecip_mm": 5.2,
    "condition": {
      "text": "Light rain",
      "icon": "//cdn.weatherapi.com/weather/64x64/day/296.png",
      "code": 1183
    }
  }
}
```
date_ must be today … +14 days.
If lat/lon are omitted, the server resolves them from location.

#### Notes:

The full API response contains many more fields (location, current, hour-by-hour, etc.).
Values above are illustrative; the real response will vary by date/time.

## Tests

Run the suite:

```bash
pytest -q
```
PostgreSQL is used in tests. Ensure your DB role has permission to create the test DB:

```bash
ALTER ROLE raincast_user CREATEDB;
```
