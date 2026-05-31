import os
from django.apps import AppConfig


class FdappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fdapp'

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':
            from .scheduler import start
            start()