from django.apps import AppConfig


class CakeModelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cake_models'

    def ready(self):
        import cake_models.signals
