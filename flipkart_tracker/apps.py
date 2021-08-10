from django.apps import AppConfig




class FlipkartTrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'flipkart_tracker'

    def ready(self):
        from flipkart_tracker import updater
        updater.start()
