"""Formularios de la aplicación Vehículos."""

from django import forms
from .models import Vehiculo, normalizar_patente


class VehiculoForm(forms.ModelForm):
    """Formulario para crear y editar vehículos con validación de patente única."""
    
    class Meta:
        model = Vehiculo
        fields = ["patente", "marca", "modelo", "anio", "numero_chasis", "numero_motor", "cliente"]
        widgets = {
            "patente": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "AB1234 o ABCD12",
                    "pattern": "[A-Z]{2}[0-9]{4}|[A-Z]{4}[0-9]{2}",
                    "title": "Formato: AA1234 (antiguo) o ABCD12 (nuevo)",
                    "style": "text-transform: uppercase;",
                }
            ),
            "marca": forms.TextInput(attrs={"class": "form-control", "placeholder": "ej: Toyota"}),
            "modelo": forms.TextInput(attrs={"class": "form-control", "placeholder": "ej: Corolla"}),
            "anio": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1900",
                    "max": "2030",
                    "placeholder": "2024"
                }
            ),
            "numero_chasis": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "17 caracteres alfanuméricos",
                    "maxlength": "17"
                }
            ),
            "numero_motor": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": "20"
                }
            ),
            "cliente": forms.Select(attrs={"class": "form-control"}),
        }
    
    def clean(self):
        """Valida duplicados por patente y valida el cliente."""
        cleaned = super().clean()
        
        patente = cleaned.get("patente")
        cliente = cleaned.get("cliente")
        
        # Validar patente
        if patente:
            patente = normalizar_patente(patente)
            cleaned["patente"] = patente
            qs = Vehiculo.objects.exclude(pk=getattr(self.instance, "pk", None)).filter(
                patente__iexact=patente
            )
            if qs.exists():
                self.add_error("patente", "Ya existe un vehículo con esa patente.")
        
        # Validar cliente
        if not cliente:
            self.add_error("cliente", "Debe seleccionar un cliente.")
        
        return cleaned