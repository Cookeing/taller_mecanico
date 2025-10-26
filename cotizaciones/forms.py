from django import forms
from .models import Cotizacion

class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = ['numero_cotizacion', 'descripcion', 'monto_total', 'estado_cotizacion', 'cliente', 'vehiculo']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }