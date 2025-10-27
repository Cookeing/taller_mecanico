"""Formularios de la aplicación Vehículos."""

from django import forms
from .models import Vehiculo, Servicio, normalizar_patente


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
                    "required": True 
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
            "cliente": forms.Select(
                attrs={
                    "class": "form-control",
                    "id": "id_cliente",
                    "required": True
                }
            ),
        }
    
    def clean_patente(self):
        """ 
        esta funcion se encarga de Valida que la patente no esté vacía y no esté duplicada 
        ."""
        patente = self.cleaned_data.get("patente")
        
        if not patente or not patente.strip():
            raise forms.ValidationError("La patente es obligatoria.")
        
        patente = normalizar_patente(patente)
        
        qs = Vehiculo.objects.exclude(pk=getattr(self.instance, "pk", None)).filter(
            patente__iexact=patente
        )
        if qs.exists():
            raise forms.ValidationError("Ya existe un vehículo con esa patente.")
        
        return patente
    
    def clean_cliente(self):
        """Valida que se haya seleccionado un cliente."""
        cliente = self.cleaned_data.get("cliente")
        
        if not cliente:
            raise forms.ValidationError("Debe seleccionar un cliente.")
        
        return cliente


class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = [
            'vehiculo',
            'fecha_servicio',
            'descripcion_trabajo',
            'diagnostico',
            'observaciones',
            'estado_servicio',
            'mano_obra',
            'repuestos'
        ]