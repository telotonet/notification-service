from django.apps import AppConfig


class NotifierConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifier'
    verbose_name = 'Сервис рассылки'

    def ready(self):
        import notifier.signals # noqa F401