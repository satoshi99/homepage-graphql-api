from .base import *


SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG')
ALLOWED_HOSTS = [
    'homepage-graphql-api.herokuapp.com',
    'mydjangomedia.s3.amazonaws.com',
]


from graphql_homepage.aws.conf import *
