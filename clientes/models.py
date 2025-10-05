"""Modelos de la aplicación Clientes."""

import re
from django.core.exceptions import ValidationError
from django.db import models


def normalizar_rut(value: str) -> str:
    """Quita puntos y espacios de un RUT y lo deja en mayúsculas."""
    return value.replace(".", "").replace(" ", "").upper()


def validar_rut(value: str) -> None:
    """Valida formato y dígito verificador del RUT chileno."""
    value = normalizar_rut(value)
    pattern = r"^\d{7,8}-[\dK]$"
    if not re.match(pattern, value):
        raise ValidationError("Formato inválido. Ej: 12345678-9 o 12.345.678-9")

    numero, dv = value.split("-")
    suma, mult = 0, 2
    for d in reversed(numero):
        suma += int(d) * mult
        mult = 2 if mult == 7 else mult + 1
    resto = 11 - (suma % 11)
    dv_calc = "0" if resto == 11 else "K" if resto == 10 else str(resto)
    if dv_calc != dv:
        raise ValidationError("Dígito verificador no válido.")

def validar_telefono(value: str) -> None:

    ### Permite fortmato de telefono internacional y local +56 y 9 dígitos
    if not re.match(r'^[\d\s\-\+\(\)]+$', value):
        raise ValidationError("El teléfono solo puede contener números, espacios, guiones, + y paréntesis.")

    # Verifica que tenga el formato correcto
    if not re.match(r'^(?:\+56\s9\d{8}|\(9\)\s\d{4}-\d{4}|\d{8})$', value):
        raise ValidationError("El teléfono debe tener un formato válido.")

    solo_numeros = re.sub(r'[^\d]', '', value)
    if len(solo_numeros) < 8:
        raise ValidationError("El teléfono debe contener al menos 8 dígitos.")


class Cliente(models.Model):
    """Entidad Cliente del taller mecánico."""

    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True, validators=[validar_rut])
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=200, blank=True, null=True)

    def clean(self):
        """Evita duplicados por nombre + teléfono."""
        if Cliente.objects.exclude(pk=self.pk).filter(
            nombre=self.nombre, telefono=self.telefono
        ).exists():
            raise ValidationError("Ya existe un cliente con el mismo nombre y teléfono.")

    def __str__(self) -> str:
        return f"{self.nombre} ({self.rut})"
