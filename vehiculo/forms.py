# vehiculo/forms.py
from django import forms
from .models import Vehiculo

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = [
            "patente",
            "cliente",
            "marca",
            "modelo",
            "anio",
            "numero_chasis",
            "numero_motor",
            "kilometraje",
        ]
        widgets = {
            "patente": forms.TextInput(attrs={"class": "form-control", "placeholder": "ABC123"}),
            "cliente": forms.Select(attrs={"class": "form-control"}),
            "marca": forms.TextInput(attrs={"class": "form-control"}),
            "modelo": forms.TextInput(attrs={"class": "form-control"}),
            "anio": forms.NumberInput(attrs={"class": "form-control"}),
            "numero_chasis": forms.TextInput(attrs={"class": "form-control"}),
            "numero_motor": forms.TextInput(attrs={"class": "form-control"}),
            "kilometraje": forms.NumberInput(attrs={"class": "form-control"}),
        }
