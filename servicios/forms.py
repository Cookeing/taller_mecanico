from django import forms
from .models import Documento, Servicio, FotoServicio
from vehiculo.models import Vehiculo


class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['vehiculo', 'descripcion_trabajo', 'fecha_servicio', 'estado']
        widgets = {
            'vehiculo': forms.Select(attrs={'class': 'form-select'}),
            'descripcion_trabajo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_servicio': forms.DateInput(
                attrs={'class': 'form-control flatpickr-date', 'placeholder': 'dd/mm/yyyy', 'inputmode': 'numeric'},
                format='%d/%m/%Y'
            ),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aceptar múltiples formatos de fecha
        self.fields['fecha_servicio'].input_formats = [
            '%d/%m/%Y',
            '%Y-%m-%d',
            '%d-%m-%Y',
        ]
        # Mostrar fecha correctamente al editar (dd/mm/YYYY)
        if self.instance and self.instance.fecha_servicio:
            self.initial['fecha_servicio'] = self.instance.fecha_servicio.strftime('%d/%m/%Y')
        
        # FILTRAR SOLO VEHÍCULOS ACTIVOS DE CLIENTES ACTIVOS
        self.fields['vehiculo'].queryset = Vehiculo.objects.filter(
            activo=True,
            cliente__activo=True
        ).select_related('cliente').order_by('patente')


class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['tipo_documento', 'fecha_documento', 'monto', 'archivo']
        widgets = {
            # Use a text input to show dd/mm/YYYY to users (browser date inputs use locale)
            'fecha_documento': forms.DateInput(attrs={'class': 'form-control flatpickr-date', 'placeholder': 'dd/mm/yyyy', 'inputmode': 'numeric'}, format='%d/%m/%Y'),
            'tipo_documento': forms.Select(attrs={'class': 'form-select'}),
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Monto (Ej: 15000)'}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Accept common date formats including Chilean dd/mm/YYYY
        self.fields['fecha_documento'].input_formats = [
            '%d/%m/%Y',
            '%Y-%m-%d',
            '%d-%m-%Y',
        ]
        # If editing an existing documento, show its date in dd/mm/YYYY
        if self.instance and getattr(self.instance, 'fecha_documento', None):
            self.initial['fecha_documento'] = self.instance.fecha_documento.strftime('%d/%m/%Y')


class FotoServicioForm(forms.Form):
    """Formulario para subir múltiples fotos a un servicio"""
    descripcion = forms.CharField(
        label='Descripción (opcional)',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Estado del motor, Rayones en puerta, etc.'
        })
    )
