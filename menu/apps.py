from django.apps import AppConfig


class MenuConfig(AppConfig):
    name = 'menu'

    def ready(self):
        import menu.signals