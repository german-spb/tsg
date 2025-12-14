from django.apps import AppConfig


class Tsg4Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tsg4'

    def ready(self):
        import tsg4.signals


