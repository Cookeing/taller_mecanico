from django import forms
from .models import Vehiculo




class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['cliente', 'patente', 'marca', 'modelo', 'anio', 'chasis', 'motor', 'kilometraje']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'patente': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'anio': forms.NumberInput(attrs={'class': 'form-control'}),
            'chasis': forms.TextInput(attrs={'class': 'form-control'}),
            'motor': forms.TextInput(attrs={'class': 'form-control'}),
            'kilometraje': forms.NumberInput(attrs={'class': 'form-control'}),
        }
