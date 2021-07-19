from django.apps import AppConfig


class StocksConfig(AppConfig):
    name = 'stocks'

    #sert pour récupérer les signaux lors de la création de l'utilisateur et créer automatiquement son profile
    def ready(self):
        import stocks.signals
