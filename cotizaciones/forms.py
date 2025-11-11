# cotizaciones/forms.py
from django import forms
from .models import Cotizacion, ItemCotizacion


class CotizacionForm(forms.ModelForm):
    """Formulario para crear y editar cotizaciones"""
    
    class Meta:
        model = Cotizacion
        fields = [
            # Datos de empresa
            'empresa_nombre',
            'empresa_rut',
            'empresa_giro',
            'empresa_direccion',
            'empresa_telefono',
            'empresa_email',
            'logo',
            
            # Datos de cotización
            'numero_cotizacion',
            'fecha_emision',
            'fecha_validez',
            
            # Relaciones
            'cliente',
            'servicio',
            
            # Condiciones
            'forma_pago',
            'plazo_pago',
            
            # Estado
            'estado_cotizacion',
        ]
        
        widgets = {
            'empresa_nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la empresa'
            }),
            'empresa_rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '12.345.678-9'
            }),
            'empresa_giro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Giro comercial'
            }),
            'empresa_direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Dirección completa'
            }),
            'empresa_telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56 9 1234 5678'
            }),
            'empresa_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'contacto@empresa.cl'
            }),
            'logo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'numero_cotizacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0001'
            }),
            'fecha_emision': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_validez': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'cliente': forms.Select(attrs={
                'class': 'form-control'
            }),
            'servicio': forms.Select(attrs={
                'class': 'form-control'
            }),
            'forma_pago': forms.Select(attrs={
                'class': 'form-control'
            }),
            'plazo_pago': forms.Select(attrs={
                'class': 'form-control'
            }),
            'estado_cotizacion': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


class ItemCotizacionForm(forms.ModelForm):
    """Formulario para items de cotización (opcional, se usa JSON)"""
    
    class Meta:
        model = ItemCotizacion
        fields = [
            'categoria',
            'descripcion',
            'cantidad',
            'precio_unitario',
        ]
        
        widgets = {
            'categoria': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Categoría'
            }),
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción del ítem'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01'
            }),
            'precio_unitario': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '1',
                'min': '0'
            }),
        }
