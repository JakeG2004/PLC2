from django.apps import AppConfig
import os


class ScadaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scada'

    def ready(self):
        pass
