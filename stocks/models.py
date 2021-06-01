from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# On ne veut pas de symbole en lettres minuscules dans la BDD, on va donc utiliser un type customisé, SymbolField, pour transformer les entrées en majuscules.
# On va ensuite rajouter une couche de RegexValidator pour être sûre que l'utilisateur ne rentre que les caractères demandés : que des lettres et un maximum de 5 caractères.

class SymbolField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(SymbolField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).upper()


# Modèle pour la view Home

class Stock(models.Model):
    symbol = SymbolField(max_length=5, validators=[RegexValidator('^[a-zA-Z]*$')])
    user = models.ForeignKey(User, default=None, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.symbol



#########################
# MODELES DU SIMULATEUR #
#########################

class Wallet(models.Model):
    user = models.ForeignKey(User, default=None, null=True, blank=True, on_delete=models.CASCADE)
    wallet = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return str(self.user)


class Portfolio(models.Model):
    user = models.ForeignKey(User, default=None, null=True, blank=True, on_delete=models.CASCADE)
    symbol = SymbolField(max_length=5, validators=[RegexValidator('^[a-zA-Z]*$')])
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=2)

    def stock_value(self):
        return self.quantity * self.price

    def __str__(self):
        return str(self.user)


