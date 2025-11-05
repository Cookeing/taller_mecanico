# cotizaciones/models.py
from django.db import models
from django.core.validators import MinValueValidator
from clientes.models import Cliente
from django.utils import timezone
import random
import string

from servicios.models import Servicio

class Cotizacion(models.Model):
    ESTADO_COTIZACION_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('APROBADA', 'Aprobada'),
        ('RECHAZADA', 'Rechazada'),
    ]
    
    FORMA_PAGO_CHOICES = [
        ('transferencia', 'Transferencia Bancaria'),
        ('efectivo', 'Efectivo'),
        ('cheque', 'Cheque'),
        ('tarjeta', 'Tarjeta de Crédito/Débito'),
        ('otro', 'Otro'),
    ]
    
    PLAZO_PAGO_CHOICES = [
        ('contado', 'Al Contado'),
        ('15', '15 días'),
        ('30', '30 días'),
        ('45', '45 días'),
        ('60', '60 días'),
        ('90', '90 días'),
    ]

    # Información de la empresa (emisor) - sin valores por defecto para permitir entrada en blanco
    empresa_nombre = models.CharField(max_length=200, blank=True)
    empresa_rut = models.CharField(max_length=20, blank=True)
    empresa_giro = models.CharField(max_length=200, blank=True)
    empresa_direccion = models.TextField(blank=True)
    empresa_telefono = models.CharField(max_length=20, blank=True)
    empresa_email = models.EmailField(blank=True)
    
    # Información de la cotización
    numero_cotizacion = models.CharField(max_length=20, unique=True, blank=True)
    fecha_emision = models.DateField(default=timezone.now)
    fecha_validez = models.DateField(blank=True, null=True)
    
    # Información del cliente (relación directa)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='cotizaciones', blank=True, null=True)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='cotizaciones', blank=True, null=True)
    
    # Condiciones de pago
    forma_pago = models.CharField(max_length=20, choices=FORMA_PAGO_CHOICES, blank=True)
    plazo_pago = models.CharField(max_length=10, choices=PLAZO_PAGO_CHOICES, blank=True)
    
    # Totales
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    monto_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    estado_cotizacion = models.CharField(max_length=10, choices=ESTADO_COTIZACION_CHOICES, default='PENDIENTE')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def generar_numero_cotizacion(self):
        """Genera un número de cotización único"""
        # Obtener el último número de cotización
        ultima_cotizacion = Cotizacion.objects.order_by('-id').first()
        if ultima_cotizacion and ultima_cotizacion.numero_cotizacion:
            try:
                # Intentar extraer el número y incrementarlo
                ultimo_numero = int(ultima_cotizacion.numero_cotizacion)
                nuevo_numero = ultimo_numero + 1
            except (ValueError, TypeError):
                # Si no es un número, empezar desde 1
                nuevo_numero = 1
        else:
            # Primera cotización
            nuevo_numero = 1
        
        return str(nuevo_numero).zfill(4)  # Formato 0001, 0002, etc.

    def save(self, *args, **kwargs):
        # Generar número de cotización si está vacío
        if not self.numero_cotizacion:
            self.numero_cotizacion = self.generar_numero_cotizacion()
        
        # Calcular automáticamente IVA y total
        if self.subtotal:
            self.iva = self.subtotal * 0.19
            self.monto_total = self.subtotal + self.iva
        
        # Intentar guardar, si hay duplicado, generar nuevo número
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            if 'duplicate' in str(e).lower() or '1062' in str(e):
                # Si hay duplicado, generar nuevo número y guardar
                self.numero_cotizacion = self.generar_numero_cotizacion()
                super().save(*args, **kwargs)
            else:
                raise e
    
    def __str__(self):
        cliente_nombre = self.cliente.nombre if self.cliente else "Sin cliente"
        return f'Cotización {self.numero_cotizacion} - {cliente_nombre}'

class ItemCotizacion(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name='items')
    categoria = models.CharField(max_length=100, default="Servicios", blank=True)
    descripcion = models.CharField(max_length=300, blank=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=1, validators=[MinValueValidator(0.01)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario
    
    def __str__(self):
        return f"{self.descripcion} - ${self.precio_unitario}"