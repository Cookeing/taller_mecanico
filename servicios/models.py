from django.db import models
from decimal import Decimal


class Servicio(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('proceso', 'En proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]

    vehiculo = models.ForeignKey(
        'vehiculo.Vehiculo',
        on_delete=models.CASCADE,
        related_name='servicios'
    )
    descripcion_trabajo = models.TextField()
    fecha_servicio = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def actualizar_total(self):
        """
        Actualiza el total solo si existen documentos con montos asociados.
        Si no hay documentos, mantiene el valor ingresado manualmente.
        """
        documentos = self.documentos.all()

        # Si existen documentos, recalculamos el total
        if documentos.exists():
            total_docs = sum(d.monto or Decimal('0.00') for d in documentos)
            # Solo actualiza si el total calculado difiere del actual
            if total_docs != self.total:
                self.total = total_docs
                self.save(update_fields=['total'])
        # Si no hay documentos, no toca el total (permite valor manual)

    def __str__(self):
        return f"Servicio #{self.id} - {self.vehiculo.patente} ({self.get_estado_display()})"

    class Meta:
        db_table = 'vehiculo_servicio'
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['-fecha_servicio']


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


class FotoServicio(models.Model):
    servicio = models.ForeignKey(
        'servicios.Servicio',
        on_delete=models.CASCADE,
        related_name='fotos'
    )
    imagen = models.ImageField(upload_to='servicios/fotos/%Y/%m/%d/')
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    fecha_captura = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_captura']
        verbose_name = 'Foto de Servicio'
        verbose_name_plural = 'Fotos de Servicios'

    def __str__(self):
        return f"Foto - Servicio #{self.servicio.id} - {self.servicio.vehiculo.patente}"