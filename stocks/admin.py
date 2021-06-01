from django.contrib import admin
from .models import Stock, Wallet, Portfolio

admin.site.register(Stock)
admin.site.register(Wallet)
admin.site.register(Portfolio)

