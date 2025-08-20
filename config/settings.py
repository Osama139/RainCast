from pathlib import Path
from dotenv import load_dotenv
import json
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


STATICFILES_DIRS = [BASE_DIR / "static"]

with open(BASE_DIR / "conf" / "app_config.json") as f:
    APP_CONFIG = json.load(f)

db = APP_CONFIG.get("database", {})
db["ENGINE"] = os.getenv("DB_ENGINE", db.get("ENGINE", "django.db.backends.postgresql"))
db["NAME"] = os.getenv("DB_NAME", db.get("NAME", "raincast"))
db["USER"] = os.getenv("DB_USER", db.get("USER", "raincast_user"))
db["PASSWORD"] = os.getenv("DB_PASSWORD", db.get("PASSWORD", "raincast123"))
db["HOST"] = os.getenv("DB_HOST", db.get("HOST", "localhost"))
db["PORT"] = int(os.getenv("DB_PORT", db.get("PORT", 5432)))

weather = APP_CONFIG.get("weather_api", {})
weather["key"] = os.getenv("WEATHER_API_KEY", weather.get("key", ""))
weather["base_url"] = os.getenv("WEATHER_BASE_URL", weather.get("base_url", "http://api.weatherapi.com/v1"))

APP_CONFIG["database"] = db
APP_CONFIG["weather_api"] = weather

DATABASES = {"default": db}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-1u)*6@=v-j%7wug+1^53#z!t13y(32k=sgj4bvi!k*!=slq!fz"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = (
    ["localhost", "127.0.0.1"]
    if DEBUG
    else os.getenv("ALLOWED_HOSTS", "3.90.44.164").split(",")
)


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",
    "raincast",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": APP_CONFIG["database"]["ENGINE"],
        "NAME": APP_CONFIG["database"]["NAME"],
        "USER": APP_CONFIG["database"]["USER"],
        "PASSWORD": APP_CONFIG["database"]["PASSWORD"],
        "HOST": APP_CONFIG["database"]["HOST"],
        "PORT": APP_CONFIG["database"]["PORT"],
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"
LOGIN_URL = "accounts:login"