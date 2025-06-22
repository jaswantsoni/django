from django.apps import AppConfig

class TestappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fitnessApp'
    def ready(self):
        import fitnessApp.signals
        import fitnessApp.my_hooks