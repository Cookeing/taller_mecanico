# cotizaciones/forms.py
from django import forms
from .models import Cotizacion
from django.utils import timezone

class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = [
            'empresa_nombre', 'empresa_rut', 'empresa_giro', 'empresa_direccion', 
            'empresa_telefono', 'empresa_email', 'fecha_emision',
            'fecha_validez', 'cliente', 'forma_pago', 'plazo_pago'
        ]
        widgets = {
            'empresa_nombre': forms.TextInput(attrs={
                'class': 'company-name-input',
                'placeholder': 'Ingrese su nombre o el de su compañía'
            }),
            'empresa_rut': forms.TextInput(attrs={
                'class': 'info-input',
                'placeholder': '12.345.678-9'
            }),
            'empresa_giro': forms.TextInput(attrs={
                'class': 'info-input', 
                'placeholder': 'Ej: Servicios de Mecánica Automotriz'
            }),
            'empresa_direccion': forms.TextInput(attrs={
                'class': 'info-input',
                'placeholder': 'Calle, Número, Comuna, Ciudad'
            }),
            'empresa_telefono': forms.TextInput(attrs={
                'class': 'info-input',
                'placeholder': '+56 9 1234 5678'
            }),
            'empresa_email': forms.EmailInput(attrs={
                'class': 'info-input',
                'placeholder': 'contacto@empresa.cl'
            }),
            'fecha_emision': forms.DateInput(attrs={
                'type': 'date',
                'class': 'date-input'
            }),
            'fecha_validez': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'date-input'
            }),
            'forma_pago': forms.Select(attrs={'class': 'form-input'}),
            'plazo_pago': forms.Select(attrs={'class': 'form-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer todos los campos no obligatorios
        for field in self.fields:
            self.fields[field].required = False