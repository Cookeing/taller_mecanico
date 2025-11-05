from django.db import models
from django.core.exceptions import ValidationError
from clientes.models import Cliente
import re


def validar_patente(value):
    # AA1234 o ABCD12
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
    chasis = models.CharField(max_length=50, blank=True, null=True)
    motor = models.CharField(max_length=50, blank=True, null=True)
    kilometraje = models.PositiveIntegerField(blank=True, null=True)

    def clean(self):
        if self.patente:
            self.patente = self.patente.upper().replace('-', '').strip()

    def __str__(self):
        return f"{self.patente} - {self.marca or ''} {self.modelo or ''}"


class Documento(models.Model):
    TIPO_DOCUMENTO = [
        ('factura', 'Factura'),
        ('boleta', 'Boleta'),
        ('certificado', 'Certificado'),
        ('presupuesto', 'Presupuesto'),
        ('informe', 'Informe técnico'),
        ('otro', 'Otro'),
    ]

    servicio = models.ForeignKey(
        'servicios.Servicio',
        on_delete=models.CASCADE,
        related_name='documentos'
    )
    tipo_documento = models.CharField(max_length=50, choices=TIPO_DOCUMENTO, default='otro')
    fecha_documento = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    archivo = models.FileField(upload_to='documentos/%Y/%m/%d/', blank=True, null=True)

    class Meta:
        ordering = ['-fecha_documento']

    def __str__(self):
        return f"{self.get_tipo_documento_display()} - {self.servicio.vehiculo.patente}"
