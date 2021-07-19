from django.contrib import admin
from .models import Stock, Wallet, Portfolio, History, Profile

admin.site.register(Stock)
admin.site.register(Wallet)
admin.site.register(Portfolio)
admin.site.register(History)
admin.site.register(Profile)
