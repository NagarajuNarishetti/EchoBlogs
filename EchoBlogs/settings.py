from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'replace-this-with-your-own-secret-key'
DEBUG = True
ALLOWED_HOSTS = ['*']

# ---------------- DJANGO TENANTS CONFIG ----------------

# SHARED_APPS → public schema
SHARED_APPS = (
    'django_tenants',      # must be first
    'tenants',             # tenant control app
    'accounts',            # accounts app (registration happens on public schema)
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

# TENANT_APPS → tenant schema
TENANT_APPS = (
    'blog',       # your tenant-specific app
)

# Combine apps correctly using tuples
INSTALLED_APPS = SHARED_APPS + TENANT_APPS

# ---------------- DATABASE ----------------
DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': 'echoblogsdb',
        'USER': 'postgres',
        'PASSWORD': 'nagi',
        'HOST': 'localhost',
        'PORT': '5434',
    }
}

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

TENANT_MODEL = "tenants.Client"        # Tenant model
TENANT_DOMAIN_MODEL = "tenants.Domain"

# ---------------- TEMPLATES ----------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # your global templates folder
        'APP_DIRS': True,  # automatically looks for templates in each app
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # required by admin
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ---------------- MIDDLEWARE ----------------
MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',  # must be first
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ---------------- URLS & WSGI ----------------
ROOT_URLCONF = 'EchoBlogs.urls'
WSGI_APPLICATION = 'EchoBlogs.wsgi.application'

# ---------------- INTERNATIONALIZATION ----------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------- STATIC FILES ----------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]  # optional: your static folder

# ---------------- DEFAULT AUTO FIELD ----------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
