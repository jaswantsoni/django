from django.apps import AppConfig


class ReviewappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviewApp'
    
    #for signals concept the first way is to register action
    def ready(self):
        import reviewApp.signals