from django import forms
from .models import Stock
from django.contrib.auth.models import User

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        exclude = ('user',)


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
