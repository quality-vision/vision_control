import logging

log = logging.getLogger(__name__)

from django.apps import AppConfig
from django.conf import settings

import os
import sys


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):
        if "runserver" not in sys.argv or os.environ.get("RUN_MAIN", None):
            return True

        log.info(f"Vision Control ({settings.GIT_REVISION})")
