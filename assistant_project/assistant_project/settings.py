"""
Django settings for assistant_project project.

Cleaned / ready for deployment:
- Secrets and environment-sensitive values read from environment variables.
- Whitenoise enabled for static files.
- Database uses dj-database-url when DATABASE_URL is provided; else sqlite for local dev.
- No runtime code (functions) inside settings.
"""

import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------- SECURITY / ENV ----------
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "unsafe-dev-key")  # set in env for prod
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

# Allow multiple hosts via environment var, defaults to localhost for dev
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# ---------- APPLICATIONS ----------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # third party
    "rest_framework",

    # your apps
    "core",
]

# ---------- MIDDLEWARE ----------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # serve static files in production
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "assistant_project.urls"

# ---------- TEMPLATES ----------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "core", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "assistant_project.wsgi.application"

# ---------- DATABASE ----------

# settings.py — safe DATABASE config
# --- DATABASE (safe fallback to sqlite if DATABASE_URL is missing/invalid) ---
import dj_database_url
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "")  # empty string if not set

if DATABASE_URL:
    try:
        DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
    except Exception:
        # If parsing fails, fall back to sqlite and log a message to the console
        import sys
        print("Warning: DATABASE_URL is invalid; falling back to sqlite.", file=sys.stderr)
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",
            }
        }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }



# ---------- PASSWORD VALIDATION ----------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------- INTERNATIONALIZATION ----------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ---------- STATIC FILES ----------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"          # where collectstatic will put files
STATICFILES_DIRS = [os.path.join(BASE_DIR, "core", "static")]  # your local static assets
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ---------- MEDIA ----------
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# ---------- DEFAULT AUTO FIELD ----------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------- EXTERNAL SERVICE CREDENTIALS (from env) ----------
# Move real secrets to environment variables; fallback to None for safety
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")  # e.g. +1...

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
# Add other API keys similarly

# ---------- LOGGING (simple) ----------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
