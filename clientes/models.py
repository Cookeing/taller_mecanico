import re
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


def normalizar_rut(value: str) -> str:
    """Quita puntos y espacios de un RUT y lo deja en mayúsculas."""
    if value:
        return value.replace(".", "").replace(" ", "").upper()
    return value


def validar_telefono(value: str) -> None:
    """Valida formato de teléfono (opcional)."""
    if not value:
        return
    if not re.match(r'^[\d\s\-\+\(\)]+$', value):
        raise ValidationError("El teléfono solo puede contener números, espacios, guiones, + y paréntesis.")
    solo_numeros = re.sub(r'[^\d]', '', value)
    if len(solo_numeros) < 8:
        raise ValidationError("El teléfono debe contener al menos 8 dígitos.")


class Cliente(models.Model):
    """Entidad Cliente del taller mecánico."""
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True, validators=[validar_telefono])
    direccion = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    contacto = models.CharField(max_length=100, blank=True, null=True, help_text="Nombre de persona de contacto")
    
    # NUEVOS CAMPOS PARA SOFT DELETE
    activo = models.BooleanField(default=True)
    fecha_eliminacion = models.DateTimeField(null=True, blank=True)

    def clean(self):
        """Evita duplicados por RUT si está presente."""
        if self.rut:
            rut_normalizado = normalizar_rut(self.rut)
            qs = Cliente.objects.exclude(pk=self.pk).filter(rut=rut_normalizado)
            if qs.exists():
                raise ValidationError("Ya existe un cliente con ese RUT.")

    def __str__(self) -> str:
        estado = "" if self.activo else " [INACTIVO]"
        if self.rut:
            return f"{self.nombre} ({self.rut}){estado}"
        return f"{self.nombre}{estado}"
