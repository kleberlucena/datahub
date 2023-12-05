from django.apps import AppConfig


class RpaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.rpa'

    def ready(self):
        import apps.rpa.signals