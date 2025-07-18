from .settings import *
import boto3
import json
import sentry_sdk
from botocore.exceptions import ClientError

DEBUG = False


ALLOWED_HOSTS = [
    "imageassistant.io", 
    "ec2-18-207-173-160.compute-1.amazonaws.com",
    "localhost",
    "127.0.0.1",
]

CSRF_TRUSTED_ORIGINS = [
    'https://imageassistant.io',
    "http://ec2-18-207-173-160.compute-1.amazonaws.com",
    "https://consent.cookiebot.com/uc.js",
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
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
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