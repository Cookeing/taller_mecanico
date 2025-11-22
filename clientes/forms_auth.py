from django import forms
from django.contrib.auth.forms import AuthenticationForm


#ESte fonrmulario lo genero para poder tener mas control sobre los atributos del formulario de login
#Asi no se ve feo
class Loginforms(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: juanperez'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: contraseña123'
        })
    )