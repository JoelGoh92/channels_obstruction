from django.apps import AppConfig


class GameConfig(AppConfig):
    name = 'game'

    # importing signals so they are available outside of the models
    def ready(self):
        from game import signals