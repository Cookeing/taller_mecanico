import os
import re
from django.core.exceptions import ValidationError
from django.db import models
from clientes.models import Cliente  # relación con Cliente

# Create your models here.


def validar_patente_chilena(value: str) -> None:
    """
    Valida formato de patente chilena.
    Formatos válidos:
    - Antiguo: AA1234 (2 letras + 4 números)
    - Nuevo: ABCD12 (4 letras + 2 números)
    """
    value = value.replace("-", "").replace(" ", "").upper().strip()
    
    # Formato antiguo: AA1234
    patron_antiguo = r'^[A-Z]{2}\d{4}$'
    # Formato nuevo: ABCD12
    patron_nuevo = r'^[A-Z]{4}\d{2}$'
    
    if not (re.match(patron_antiguo, value) or re.match(patron_nuevo, value)):
        raise ValidationError(
            "Formato de patente inválido. Use AA1234 o ABCD12"
        )


def normalizar_patente(value: str) -> str:
    """Normaliza la patente removiendo espacios, guiones y convirtiendo a mayúsculas."""
    return value.replace("-", "").replace(" ", "").upper().strip()


class Vehiculo(models.Model):
    """Entidad Vehículo del taller mecánico."""

    patente = models.CharField(
        max_length=10, 
        unique=True,
        validators=[validar_patente_chilena],
        help_text="Formato: AA1234 o ABCD12"
    )
    cliente = models.ForeignKey("clientes.Cliente", on_delete=models.CASCADE, related_name="vehiculos")

    marca = models.CharField(max_length=50, blank=True, null=True)
    modelo = models.CharField(max_length=50, blank=True, null=True)
    anio = models.PositiveIntegerField(blank=True, null=True)

    # Opcionales extra
    numero_chasis = models.CharField(max_length=30, blank=True, null=True)
    numero_motor = models.CharField(max_length=30, blank=True, null=True)
    kilometraje = models.PositiveIntegerField(blank=True, null=True)

    fecha_registro = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """Normaliza la patente y valida unicidad."""
        if self.patente:
            self.patente = normalizar_patente(self.patente)
            
            # Validar que no exista otra patente igual
            qs = Vehiculo.objects.exclude(pk=self.pk).filter(patente=self.patente)
            if qs.exists():
                raise ValidationError({"patente": "Ya existe un vehículo con esta patente."})
    
    def save(self, *args, **kwargs):
        """Normaliza la patente antes de guardar."""
        if self.patente:
            self.patente = normalizar_patente(self.patente)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patente} - {self.marca or 'N/A'} {self.modelo or ''}"
    
    
ESTADO_SERVICIO_CHOICES = (
    ('PENDIENTE', 'Pendiente'),
    ('EN_PROCESO', 'En Proceso'),
    ('COMPLETADO', 'Completado'),
    ('CANCELADO', 'Cancelado'),
)

class Servicio(models.Model):
    """Representa un trabajo o intervención realizado a un vehículo (Tabla 'servicio')."""

    # 1. Relación OBLIGATORIA (Ya existe: Vehiculo)
    vehiculo = models.ForeignKey(
        'Vehiculo',
        on_delete=models.CASCADE,
        related_name="servicios" 
    )

    # 2. Relaciones PENDIENTES (Las hacemos Opcionales y Comentadas)
    # Por ahora, usamos campos vacíos (null=True, blank=True) para evitar errores.
    # Cuando creemos los modelos 'OrdenTrabajo' y 'Tecnico', se deben reemplazar estos campos.
    orden_tabajo_pendiente_id = models.IntegerField(null=True, blank=True, verbose_name="FK Orden Trabajo (Pendiente)")
    tecnico_responsable_pendiente_id = models.IntegerField(null=True, blank=True, verbose_name="FK Técnico Responsable (Pendiente)")

    # Atributos principales según el esquema
    fecha_servicio = models.DateTimeField()
    descripcion_trabajo = models.TextField()
    diagnostico = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    estado_servicio = models.CharField(
        max_length=20,
        choices=ESTADO_SERVICIO_CHOICES,
        default='PENDIENTE'
    )
    
    # Campos de costos
    mano_obra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    repuestos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total = (self.mano_obra or 0) + (self.repuestos or 0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Servicio ID {self.pk} a {self.vehiculo.patente}"


def documento_upload_to(instance, filename):
    patente = instance.servicio.vehiculo.patente.replace('-', '').replace(' ', '').upper()
    return f'documentos/{patente}/{filename}'


def ruta_documento(instance, filename):
    # Obtiene la patente del vehículo
    try:
        patente = instance.servicio.vehiculo.patente
    except AttributeError:
        patente = "sin_patente"

    # Normaliza el tipo de documento (sin espacios ni tildes)
    tipo = instance.tipo_documento.lower().replace(" ", "_")

    # Devuelve la ruta: documentos/patente/tipo/archivo
    return os.path.join('documentos', patente, tipo, filename)


TIPO_DOCUMENTO_CHOICES = [
    ('factura', 'Factura'),
    ('presupuesto', 'Presupuesto'),
    ('informe', 'Informe'),
    ('cotizacion', 'Cotización'),
    ('manual', 'Manual Técnico'),
    ('otro', 'Otro'),
]


class Documento(models.Model):
    tipo_documento = models.CharField(
        max_length=50,
        choices=TIPO_DOCUMENTO_CHOICES,
        default='otro'
    )
    fecha_documento = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    archivo = models.FileField(upload_to=ruta_documento)
    servicio = models.ForeignKey('Servicio', on_delete=models.CASCADE, related_name='documentos')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_documento', '-fecha_subida']

    def __str__(self):
        return f"{self.tipo_documento} - {self.servicio.vehiculo.patente}"
