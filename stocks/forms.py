from django import forms
from .models import Stock, Profile
from django.contrib.auth.models import User

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        exclude = ('user',)


class RegisterForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirmation = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    #Confirmation du mot de passe
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")
        if password != password_confirmation:
            self.add_error('password', "Passwords are not matching")


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

#Pour mettre à jour le pseudo et l'email 
class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ('username', 'email')
        

#Pour mettre à jour la photo de profile
class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image',)
