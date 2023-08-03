from django.apps import AppConfig


class RpaManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.rpa_manager'

    def ready(self):
        import apps.rpa_manager.signals