from .base import *


SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG')
ALLOWED_HOSTS = []


from graphql_homepage.aws.conf import *
