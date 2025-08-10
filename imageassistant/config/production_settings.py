from .settings import *
import boto3
import json
import sentry_sdk
from botocore.exceptions import ClientError
import os 

DEBUG = False


ALLOWED_HOSTS = [
    "imageassistant.io", 
    "localhost",
    "127.0.0.1",
]

CSRF_TRUSTED_ORIGINS = [
    'https://imageassistant.io',
    "https://consent.cookiebot.com/uc.js",
]

CORS_ALLOWED_ORIGINS = [
    "https://imageassistant.io"
]


# Production CORS settings
CORS_ALLOW_ALL_ORIGINS = False

# Only allow your actual production domains
CORS_ALLOWED_ORIGINS = [
    "https://imageassistant.io",
]

HANDLER500 = 'config.views.handler500'

def get_secret():

    secret_name = "imageassistant-secrets"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secrets = get_secret_value_response['SecretString']
    return json.loads(secrets)


SECRETS = get_secret()
sentry_sdk.init(
    dsn=SECRETS['SENTRY_DSN'],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    _experiments={
        # Set continuous_profiling_auto_start to True
        # to automatically start the profiler on when
        # possible.
        "continuous_profiling_auto_start": True,
    },
)


SECRET_KEY = SECRETS['SECRET_KEY']

# Reconfigure JWT with the correct SECRET_KEY
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,  # Use the production SECRET_KEY
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': SECRETS["DB_NAME"],
        'USER': SECRETS["DB_USER"],
        'PASSWORD': SECRETS["DB_PASSWORD"],
        'HOST': SECRETS["DB_HOST"],
        'PORT': '5432',
    }
}
AWS_ACCESS_KEY_ID = SECRETS['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = SECRETS['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = SECRETS['AWS_STORAGE_BUCKET_NAME']
AWS_S3_CUSTOM_DOMAIN = "{}.s3.us-east-1.amazonaws.com".format(AWS_STORAGE_BUCKET_NAME)
# need a signature for kms
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=0',

}
AWS_LOCATION = 'static'
STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'config.storage_backends.StaticStorage'
DEFAULT_FILE_STORAGE = 'config.storage_backends.MediaStorage'
CLOUDFRONT_DOMAIN = SECRETS['CLOUDFRONT_DOMAIN']
COMPRESS_URL = f"https://{CLOUDFRONT_DOMAIN}/static/"
COMPRESS_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
COMPRESS_ROOT = BASE_DIR / 'static'

STATIC_HOST = CLOUDFRONT_DOMAIN
STATIC_URL = "https://"+STATIC_HOST + "/static/"
MEDIA_URL = "https://"+STATIC_HOST + "/media/"
IMAGE_PROCESSED_FOLDER_NAME = SECRETS['IMAGE_PROCESSED_FOLDER_NAME']
STRIPE_SECRET_KEY = SECRETS['STRIPE_SECRET_KEY']
DOMAIN = "https://imageassistant.io"
STRIPE_PRICE_ID = SECRETS['STRIPE_PRICE_ID']
STRIPE_PUBLIC_KEY = SECRETS['STRIPE_PUBLISHED_KEY']
STABILITY_AI_KEY = SECRETS['STABILITY_AI_KEY']
MAILERSEND_SMTP_PORT = SECRETS['MAILERSEND_SMTP_PORT']
MAILERSEND_SMTP_USERNAME = SECRETS['MAILERSEND_SMTP_USERNAME']
MAILERSEND_SMTP_PASSWORD = SECRETS['MAILERSEND_SMTP_PASSWORD']
MAILERSEND_SMTP_HOST = SECRETS['MAILERSEND_SMTP_HOST']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = MAILERSEND_SMTP_HOST
EMAIL_PORT = MAILERSEND_SMTP_PORT
EMAIL_USE_TLS = True
EMAIL_HOST_USER = MAILERSEND_SMTP_USERNAME
EMAIL_HOST_PASSWORD = MAILERSEND_SMTP_PASSWORD
EMAIL_DOMAIN = "imageassistant.io"
GOOGLE_LOGIN_PROTOCOl = "https"
GOOGLE_LOGIN_DOMAIN = EMAIL_DOMAIN
GOOGLE_LOGIN_CALLBACK_PATH = "users/google/login/"
GOOGLE_LOGIN_REDIRECT_URI = f"{GOOGLE_LOGIN_PROTOCOl}://{GOOGLE_LOGIN_DOMAIN}/{GOOGLE_LOGIN_CALLBACK_PATH}"
GOOGLE_CLIENT_ID = SECRETS['GOOGLE_CLIENT_ID']
DEFAULT_FROM_EMAIL = SECRETS['DEFAULT_FROM_EMAIL']
DEFAULT_TO_EMAIL = SECRETS['DEFAULT_TO_EMAIL']
