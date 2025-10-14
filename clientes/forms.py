"""Formularios de la aplicación Clientes."""

from django import forms
from .models import Cliente, normalizar_rut


class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ["nombre", "rut", "telefono", "direccion"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "rut": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "12.345.678-5", "pattern": r"[\d\s\-\+\(\)]+", "title": "Solo números, espacios, guiones, + y paréntesis"
                }
            ),
                    "telefono": forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "tel",
                "pattern": "[0-9]{8,15}",  # 
                "title": "Solo números, mínimo 8 dígitos",
                "placeholder": "92239994"
            }),
            "direccion": forms.TextInput(attrs={"class": "form-control"}),
            
        }

    def clean(self):
        """Valida duplicados por RUT y por nombre + teléfono."""
        cleaned = super().clean()

        rut = cleaned.get("rut")
        nombre = cleaned.get("nombre")
        telefono = cleaned.get("telefono")

        # Validar RUT
        if rut:
            rut = normalizar_rut(rut)
            cleaned["rut"] = rut
            qs = Cliente.objects.exclude(pk=getattr(self.instance, "pk", None)).filter(
                rut__iexact=rut
            )
            if qs.exists():
                self.add_error("rut", "Ya existe un cliente con ese RUT.")

        # Validar nombre + teléfono
        if nombre and telefono:
            qs = Cliente.objects.exclude(pk=getattr(self.instance, "pk", None)).filter(
                nombre=nombre, telefono=telefono
            )
            if qs.exists():
                self.add_error(
                    "telefono", "Ya existe un cliente con el mismo nombre y teléfono."
                )

        return cleaned
