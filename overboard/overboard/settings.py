"""
Django settings for overboard project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1d($$1=_0+jf!)b*^gh9p!5_w0w04x&0z*27!-=+hx#hqd5=-t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pagination_bootstrap',
    'social_django',
    #'social_django_mongoengine',
    'core',
    'tags',
    'users',
    'posts',
    'notifications',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination_bootstrap.middleware.PaginationMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'overboard.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['./templates/', '/templates/tag'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'overboard.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'overboard2',
        'USER': 'postgres',
        'PASSWORD': 'P@ssw0rd',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = '/'

# SOCIAL_AUTH_STORAGE = 'social_django_mongoengine.models.DjangoStorage'
# SOCIAL_AUTH_POSTGRES_JSONFIELD = True

# SOCIAL_AUTH_PIPELINE = (
#     'social_auth.backends.pipeline.social.social_auth_user',
#     'social_auth.backends.pipeline.associate.associate_by_email',
#     'social_auth.backends.pipeline.user.get_username',
#     'social_auth.backends.pipeline.user.create_user',
#     'social_auth.backends.pipeline.social.associate_user',
#     'social_auth.backends.pipeline.user.update_user_details',
# )

# True - redirects to https, False - redirects to http
SOCIAL_AUTH_REDIRECT_IS_HTTPS = False

# Github sign in
SOCIAL_AUTH_GITHUB_KEY = '28d673e68c49d4574d62'
SOCIAL_AUTH_GITHUB_SECRET = 'd6e99dbe3c633bfc7636520a71262d12e51cb2e7'

# Facebok sign in
SOCIAL_AUTH_FACEBOOK_KEY = '579277219095332'
SOCIAL_AUTH_FACEBOOK_SECRET = '9217a68ef7e4269c5935a9514a6b6d14'

# Twitter sign in
SOCIAL_AUTH_TWITTER_KEY = '1H15uTpz1PYdhxzOKbTAccCZC'
SOCIAL_AUTH_TWITTER_SECRET = '6hxZZDnkyQ1ei9jyjtYDHGM0kQ9pdZTMglQKETa273lAtnubtb'

# Google sign in
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '243966779184-71l2uotc2f6t39ngleci66a3d4f1vnup.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'KKNYThbtRNWXcdlghl3ZpDLf'
SOCIAL_AUTH_GOOGLE_OAUTH2_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
'https://www.googleapis.com/auth/userinfo.email',
'https://www.googleapis.com/auth/userinfo.profile'
]
SOCIAL_AUTH_GOOGLE_PLUS_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_GOOGLE_PLUS_SCOPE = [
'https://www.googleapis.com/auth/plus.login',
'https://www.googleapis.com/auth/userinfo.email',
'https://www.googleapis.com/auth/userinfo.profile'
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request"
)

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.open_id.OpenIdAuth',
    'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.google.GoogleOAuth',
    'social_core.backends.yahoo.YahooOpenId',

    'django.contrib.auth.backends.ModelBackend',

)