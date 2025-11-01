import re
from django.core.exceptions import ValidationError
from django.db import models

def normalizar_rut(value: str) -> str:
    """Quita puntos y espacios de un RUT y lo deja en mayúsculas."""
    if value:
        return value.replace(".", "").replace(" ", "").upper()
    return value

def validar_rut(value: str) -> None:
    """Valida formato y dígito verificador del RUT chileno."""
    if not value:  # Si está vacío, no validar
        return
        
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
    """Valida formato de teléfono (opcional)."""
    if not value:  # Si está vacío, no validar
        return
        
    # Permite formato de teléfono internacional y local
    if not re.match(r'^[\d\s\-\+\(\)]+$', value):
        raise ValidationError("El teléfono solo puede contener números, espacios, guiones, + y paréntesis.")

    solo_numeros = re.sub(r'[^\d]', '', value)
    if len(solo_numeros) < 8:
        raise ValidationError("El teléfono debe contener al menos 8 dígitos.")

class Cliente(models.Model):
    """Entidad Cliente del taller mecánico."""

    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, blank=True, null=True, validators=[validar_rut])
    telefono = models.CharField(max_length=15, blank=True, null=True, validators=[validar_telefono])
    direccion = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    contacto = models.CharField(max_length=100, blank=True, null=True, help_text="Nombre de persona de contacto")

    def clean(self):
        """Evita duplicados por RUT si está presente."""
        if self.rut:
            rut_normalizado = normalizar_rut(self.rut)
            qs = Cliente.objects.exclude(pk=self.pk).filter(rut=rut_normalizado)
            if qs.exists():
                raise ValidationError("Ya existe un cliente con ese RUT.")

    def __str__(self) -> str:
        if self.rut:
            return f"{self.nombre} ({self.rut})"
        return f"{self.nombre}"