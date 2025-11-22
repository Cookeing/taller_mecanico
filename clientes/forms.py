from django import forms
from .models import Cliente, normalizar_rut

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nombre", "rut", "telefono", "direccion", "email", "contacto"]
        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "form-control",
                "required": "required"
            }),
            "rut": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "12.345.678-5",
                # Solo deja el formateo JS, sin validación
            }),
            "telefono": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "+56 9 1234 5678"
            }),
            "direccion": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Calle, Número, Comuna, Ciudad"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "cliente@email.cl"
            }),
            "contacto": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nombre de persona de contacto"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].required = True
        self.fields['rut'].required = False
        self.fields['telefono'].required = False
        self.fields['direccion'].required = False
        self.fields['email'].required = False
        self.fields['contacto'].required = False

    def clean(self):
        cleaned_data = super().clean()
        rut = cleaned_data.get("rut")
        if rut:
            rut = normalizar_rut(rut)
            cleaned_data["rut"] = rut
            qs = Cliente.objects.exclude(pk=getattr(self.instance, "pk", None)).filter(rut=rut)
            if qs.exists():
                self.add_error("rut", "Ya existe un cliente con ese RUT.")
        return cleaned_data
