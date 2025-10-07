from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url
import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from cloudinary_storage.storage import MediaCloudinaryStorage


# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Load environment variables ---
load_dotenv()

# --- Security ---
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-temp-key')
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS')
if ALLOWED_HOSTS:
    ALLOWED_HOSTS = ALLOWED_HOSTS.split(',')
else:
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'raise-nanobiotech.up.railway.app', 'rcn-success.onrender.com', 'rcn-web.up.railway.app']


CSRF_TRUSTED_ORIGINS = [
    f"https://{host}" for host in ALLOWED_HOSTS if "railway.app" in host
]

# --- Installed Apps ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',
    'startups',
    'products',
    'orders',
    'events',
    'favorites',
    'cart',
    'users.apps.UsersConfig',
    'cloudinary_storage',
    'cloudinary',
    'sendgrid_backend',
    'core',
]

# --- Middleware ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rcnb.urls'

# --- Templates ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart_item_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'rcnb.wsgi.application'

# --- Database ---
if os.environ.get("DATABASE_URL"):
    DATABASES = {
        "default": dj_database_url.config(
            default=os.environ["DATABASE_URL"],
            conn_max_age=600,
            conn_health_checks=True
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'raise_db',
            'HOST': 'localhost',
            'PORT': '5432',
            'USER': 'postgres',
            'PASSWORD': 'ANON77',
        }
    }

# --- Password Validators ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internationalization ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- Static Files (and WhiteNoise) ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# --- DIAGNOSTIC PRINTS (REMOVE LATER) ---
print("--- SETTINGS.PY DIAGNOSTICS ---")
print(f"DJANGO_ENV variable is: {os.environ.get('DJANGO_ENV')}")
print(f"DEBUG variable is: {DEBUG}")
print("--- END DIAGNOSTICS ---")


if os.environ.get('DJANGO_ENV') == 'production':
    # Production settings (Railway)
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
        'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
        'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
    }
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
else:
    # Development settings (local)
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'

# --- DIAGNOSTIC PRINT FOR STORAGE ---
print(f"FINAL DEFAULT_FILE_STORAGE is: {DEFAULT_FILE_STORAGE}")

# --- Email (SendGrid) ---
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'webmaster@localhost')
SENDGRID_SANDBOX_MODE_IN_DEBUG = False

# --- Authentication ---
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'products:product_list'
LOGOUT_REDIRECT_URL = 'users:login'

# --- Default Primary Key ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Logging ---
# --- Logging ---
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        # --- ADD THESE TWO LOGGERS ---
        'cloudinary': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'cloudinary_storage': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

print("CLOUDINARY_CLOUD_NAME =", os.getenv("CLOUDINARY_CLOUD_NAME"))

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL = '/media/'
