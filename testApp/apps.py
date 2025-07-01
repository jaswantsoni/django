from django.apps import AppConfig


class TestappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'testApp'


    #for calling signals
    def ready(self):
        import testApp.signals
    #for calling hooks
        import testApp.hooks
