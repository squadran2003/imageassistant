from .settings import *
import boto3
import json
from botocore.exceptions import ClientError

DEBUG = False

ALLOWED_HOSTS = ["imageassistant.io", "ec2-18-207-173-160.compute-1.amazonaws.com"]

CSRF_TRUSTED_ORIGINS = [
    'https://imageassistant.io',
    "http://ec2-18-207-173-160.compute-1.amazonaws.com"
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    "whitenoise.runserver_nostatic",
    'django.contrib.staticfiles',
    'django_components',
    'rest_framework',
    'storages',
    'django_celery_beat',
    'images',
    'api',
]

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     "whitenoise.middleware.WhiteNoiseMiddleware",
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]



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
    'CacheControl': 'max-age=86400',

}
AWS_LOCATION = 'static'
STATIC_URL = "https://{}/{}/".format(AWS_S3_CUSTOM_DOMAIN, 'static')
MEDIA_URL = "https://{}/{}/".format(AWS_S3_CUSTOM_DOMAIN, 'media')
STATIC_FILES_STORAGE = 'config.storage_backends.StaticStorage'
DEFAULT_FILE_STORAGE = 'config.storage_backends.MediaStorage'
IMAGE_PROCESSED_FOLDER_NAME = SECRETS['IMAGE_PROCESSED_FOLDER_NAME']
STRIPE_SECRET_KEY = SECRETS['STRIPE_SECRET_KEY']
DOMAIN = "https://imageassistant.io"
STRIPE_PRICE_ID = SECRETS['STRIPE_PRICE_ID']
STRIPE_PUBLIC_KEY = SECRETS['STRIPE_PUBLISHED_KEY']
# STATIC_HOST = SECRETS['CLOUDFRONT_DOMAIN']
# STATIC_URL = STATIC_HOST + "/static/"
