from django import forms
from servicios.models import Servicio
from .models import Vehiculo, Documento

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['vehiculo', 'descripcion_trabajo', 'fecha_servicio', 'estado']
        widgets = {
            'vehiculo': forms.Select(attrs={'class': 'form-select'}),
            'descripcion_trabajo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_servicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }


class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['tipo_documento', 'fecha_documento', 'monto', 'archivo']
        widgets = {
            'fecha_documento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tipo_documento': forms.Select(attrs={'class': 'form-select'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


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
