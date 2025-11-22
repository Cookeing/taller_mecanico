from django.db import models
from django.core.exceptions import ValidationError
from clientes.models import Cliente
import re


def validar_patente(value):
    pattern = r'^([A-Z]{2}\d{4}|[A-Z]{4}\d{2})$'
    if not re.match(pattern, value.upper()):
        raise ValidationError('Formato de patente inválido. Ejemplo: AA1234 o ABCD12')


class Vehiculo(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='vehiculos'
    )
    patente = models.CharField(
        max_length=10,
        unique=True,
        validators=[validar_patente]
    )
    marca = models.CharField(max_length=50, blank=True, null=True)
    modelo = models.CharField(max_length=50, blank=True, null=True)
    anio = models.PositiveIntegerField(blank=True, null=True)
    chasis = models.CharField(max_length=50, blank=True, null=True, db_column='numero_chasis')
    motor = models.CharField(max_length=50, blank=True, null=True, db_column='numero_motor')
    kilometraje = models.PositiveIntegerField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    # NUEVOS CAMPOS PARA SOFT DELETE
    activo = models.BooleanField(default=True)
    fecha_eliminacion = models.DateTimeField(null=True, blank=True)

    def clean(self):
        if self.patente:
            self.patente = self.patente.upper().replace('-', '').strip()

    def __str__(self):
        estado = "" if self.activo else " [INACTIVO]"
        return f"{self.patente} - {self.marca or ''} {self.modelo or ''}{estado}"
