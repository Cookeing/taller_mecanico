from django import forms
from decimal import Decimal, InvalidOperation
from .models import Documento, Servicio


class ServicioForm(forms.ModelForm):
    total = forms.CharField(
        label="Total ($)",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 15.000 o 15000'
        }),
    )

    class Meta:
        model = Servicio
        fields = ['vehiculo', 'descripcion_trabajo', 'fecha_servicio', 'estado', 'total']
        widgets = {
            'vehiculo': forms.Select(attrs={'class': 'form-select'}),
            'descripcion_trabajo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            # El navegador usa formato ISO 8601, por eso definimos input_formats explícitamente
            'fecha_servicio': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d'
            ),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🔹 Aceptar múltiples formatos al recibir la fecha
        self.fields['fecha_servicio'].input_formats = [
            '%Y-%m-%d',  # Formato ISO del input type=date
            '%d-%m-%Y',  # Formato visual común en Chile
            '%d/%m/%Y',
        ]

        # 🔹 Mostrar correctamente la fecha al editar
        if self.instance and self.instance.fecha_servicio:
            self.initial['fecha_servicio'] = self.instance.fecha_servicio.strftime('%Y-%m-%d')

        # 🔹 Mostrar total formateado con puntos de miles
        if self.instance and self.instance.total is not None:
            self.fields['total'].initial = f"{int(self.instance.total):,}".replace(",", ".")

    def clean_total(self):
        """Convierte el total en Decimal aceptando puntos o comas."""
        total = self.cleaned_data.get('total', '')

        if not total:
            return Decimal('0.00')

        total = total.replace('.', '').replace(',', '.')
        try:
            valor = Decimal(total)
        except (InvalidOperation, ValueError):
            raise forms.ValidationError("Ingrese un número válido para el total (ej: 15.000 o 15000).")

        if valor.as_tuple().exponent < -2:
            raise forms.ValidationError("Use máximo 2 decimales.")

        return valor


# class ServicioForm(forms.ModelForm):
#     class Meta:
#         model = Servicio
#         fields = ['vehiculo', 'descripcion_trabajo', 'fecha_servicio', 'estado']
#         widgets = {
#             'vehiculo': forms.Select(attrs={'class': 'form-select'}),
#             'descripcion_trabajo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#             'fecha_servicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'estado': forms.Select(attrs={'class': 'form-select'}),
#         }


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