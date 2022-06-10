from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

LOGGING["loggers"]["api"]["level"] = environment.str(
    "DJANGO_LOG_LEVEL", default="DEBUG"
)

LOGGING["loggers"]["hooks"]["level"] = environment.str(
    "DJANGO_LOG_LEVEL", default="DEBUG"
)
