from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='usuario',
        widget=forms.TextInput(
            attrs = {
                'placeholder': 'Nombre de usuario',
                'class':'form-control'
            }
        )
    )

    password = forms.CharField(
        label='', 
        widget=forms.PasswordInput(
            attrs = {
                'placeholder': 'Contraseña',
                'class':'form-control'
            }
        )
    )
