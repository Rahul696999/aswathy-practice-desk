import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = os.environ.get("LOCAL_DEV") == "1"
ALLOWED_HOSTS = os.environ.get("DJANGO_HOSTS", "localhost,127.0.0.1").split(",")
ROOT_URLCONF = "urls"
INSTALLED_APPS = ["django.contrib." + name for name in ("admin","auth","contenttypes","sessions","messages","staticfiles")] + ["appointments"]
MIDDLEWARE = ["django.middleware.security.SecurityMiddleware","django.contrib.sessions.middleware.SessionMiddleware","django.middleware.common.CommonMiddleware","django.middleware.csrf.CsrfViewMiddleware","django.contrib.auth.middleware.AuthenticationMiddleware","django.contrib.messages.middleware.MessageMiddleware","django.middleware.clickjacking.XFrameOptionsMiddleware"]
TEMPLATES = [{"BACKEND":"django.template.backends.django.DjangoTemplates","APP_DIRS":True,"OPTIONS":{"context_processors":["django.template.context_processors.request","django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages"]}}]
DATABASES = {"default":{"ENGINE":"django.db.backends.sqlite3","NAME":os.environ.get("DATABASE_PATH", BASE_DIR / "practice.sqlite3")}}
TIME_ZONE = "Asia/Kolkata"
USE_TZ = True
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SESSION_COOKIE_SECURE = CSRF_COOKIE_SECURE = SECURE_SSL_REDIRECT = not DEBUG
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SECURE_REFERRER_POLICY = "same-origin"
AUTH_PASSWORD_VALIDATORS = [{"NAME":"django.contrib.auth.password_validation."+v} for v in ("MinimumLengthValidator","CommonPasswordValidator","UserAttributeSimilarityValidator","NumericPasswordValidator")]
