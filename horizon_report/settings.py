"""
Django settings for horizon_report project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from configurations import Configuration, values

class Dev(Configuration):
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    SECRET_KEY = "django-insecure-5n41p&8@@e^0g0)7j(i%5lc&ne_#8pbbh=65$7lc&n^y6q=j6u"
    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(True)

    ALLOWED_HOSTS = values.ListValue([])

    # Application definition

    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django_htmx",
        "cfc_report",
    ]

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "django_htmx.middleware.HtmxMiddleware",
    ]

    ROOT_URLCONF = "horizon_report.urls"

    # dirs added: /static /templates
    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [BASE_DIR / "templates", BASE_DIR / "static"],
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

    WSGI_APPLICATION = "horizon_report.wsgi.application"

    # Database
    # https://docs.djangoproject.com/en/5.1/ref/settings/#databases

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

    # Password validation
    # https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME":
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME":
            "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME":
            "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME":
            "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]

    # Internationalization
    # https://docs.djangoproject.com/en/5.1/topics/i18n/

    LANGUAGE_CODE = "en-ca"

    TIME_ZONE = "UTC"

    USE_I18N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/5.1/howto/static-files/

    STATIC_URL = "static/"
    STATICFILES_DIRS = [BASE_DIR / "static"]

    # Default primary key field type
    # https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

class Prod(Dev):
    DEBUG = False
    SECRET_KEY = values.SecretValue()
    ALLOWED_HOSTS = values.ListValue()
