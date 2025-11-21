# cotizaciones/models.py - VERSIÓN MEJORADA CON DATOS DE USUARIO

from django.db import models
from django.core.validators import MinValueValidator
from clientes.models import Cliente
from servicios.models import Servicio
from django.utils import timezone
from django.utils.html import strip_tags
from urllib.parse import quote



class Cotizacion(models.Model):
    """Modelo para cotizaciones de servicios con datos de usuario/empresa"""
    
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
    
    # =========================================
    # INFORMACIÓN DE LA EMPRESA/USUARIO
    # =========================================
    empresa_nombre = models.CharField(
        max_length=200, 
        blank=True,
        verbose_name="Nombre de la empresa"
    )
    empresa_rut = models.CharField(
        max_length=20, 
        blank=True,
        verbose_name="RUT de la empresa"
    )
    empresa_giro = models.CharField(
        max_length=200, 
        blank=True,
        verbose_name="Giro de la empresa"
    )
    empresa_direccion = models.TextField(
        blank=True,
        verbose_name="Dirección de la empresa"
    )
    empresa_telefono = models.CharField(
        max_length=20, 
        blank=True,
        verbose_name="Teléfono de la empresa"
    )
    empresa_email = models.EmailField(
        blank=True,
        verbose_name="Email de la empresa"
    )
    empresa_sitio_web = models.URLField(
        blank=True,
        null=True,
        verbose_name="Sitio web"
    )
    empresa_contacto_persona = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Persona de contacto"
    )
    logo = models.ImageField(
        upload_to='cotizaciones/logos/', 
        blank=True, 
        null=True,
        verbose_name="Logo de la empresa"
    )
    
    # =========================================
    # INFORMACIÓN DE LA COTIZACIÓN
    # =========================================
    numero_cotizacion = models.CharField(
        max_length=20, 
        unique=True, 
        blank=True,
        verbose_name="Número de cotización"
    )
    fecha_emision = models.DateField(
        default=timezone.now,
        verbose_name="Fecha de emisión"
    )
    fecha_validez = models.DateField(
        blank=True, 
        null=True,
        verbose_name="Fecha de validez"
    )
    
    # =========================================
    # RELACIONES
    # =========================================
    cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.CASCADE, 
        related_name='cotizaciones', 
        blank=True, 
        null=True,
        verbose_name="Cliente"
    )
    servicio = models.ForeignKey(
        Servicio, 
        on_delete=models.CASCADE, 
        related_name='cotizaciones', 
        blank=True, 
        null=True,
        verbose_name="Servicio relacionado"
    )
    
    # =========================================
    # CONDICIONES DE PAGO
    # =========================================
    forma_pago = models.CharField(
        max_length=20, 
        choices=FORMA_PAGO_CHOICES, 
        blank=True,
        verbose_name="Forma de pago"
    )
    plazo_pago = models.CharField(
        max_length=10, 
        choices=PLAZO_PAGO_CHOICES, 
        blank=True,
        verbose_name="Plazo de pago"
    )
    
    # =========================================
    # NOTAS Y TÉRMINOS
    # =========================================
    notas_adicionales = models.TextField(
        blank=True,
        verbose_name="Notas adicionales",
        help_text="Observaciones, términos o condiciones especiales"
    )
    
    # =========================================
    # TOTALES
    # =========================================
    subtotal = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0,
        verbose_name="Subtotal"
    )
    iva = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0,
        verbose_name="IVA (19%)"
    )
    monto_total = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0,
        verbose_name="Monto total"
    )
    
    # =========================================
    # ESTADO Y AUDITORÍA
    # =========================================
    estado_cotizacion = models.CharField(
        max_length=10, 
        choices=ESTADO_COTIZACION_CHOICES, 
        default='PENDIENTE',
        verbose_name="Estado"
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última modificación"
    )
    
    class Meta:
        verbose_name = "Cotización"
        verbose_name_plural = "Cotizaciones"
        ordering = ['-fecha_creacion']
    
    def generar_numero_cotizacion(self):
        """Genera un número de cotización único secuencial"""
        ultima_cotizacion = Cotizacion.objects.order_by('-id').first()
        if ultima_cotizacion and ultima_cotizacion.numero_cotizacion:
            try:
                # Intentar extraer el número y sumar 1
                ultimo_numero = int(ultima_cotizacion.numero_cotizacion)
                nuevo_numero = ultimo_numero + 1
            except (ValueError, TypeError):
                # Si no es un número, empezar desde 1
                nuevo_numero = 1
        else:
            # Primera cotización
            nuevo_numero = 1
        
        # Formato con ceros a la izquierda (ej: 0001, 0002, etc.)
        return str(nuevo_numero).zfill(4)
    
    def save(self, *args, **kwargs):
        """Sobrescribir save para generar número y calcular totales"""
        
        # Generar número de cotización si está vacío
        if not self.numero_cotizacion:
            self.numero_cotizacion = self.generar_numero_cotizacion()
        
        # Calcular automáticamente IVA y total
        if self.subtotal:
            self.iva = self.subtotal * 0.19
            self.monto_total = self.subtotal + self.iva
        else:
            self.iva = 0
            self.monto_total = 0
        
        # Intentar guardar
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            # Si hay error de duplicado (número único), generar nuevo número
            if 'duplicate' in str(e).lower() or '1062' in str(e):
                self.numero_cotizacion = self.generar_numero_cotizacion()
                super().save(*args, **kwargs)
            else:
                raise e
    
    def __str__(self):
        cliente_nombre = self.cliente.nombre if self.cliente else "Sin cliente"
        return f'Cotización {self.numero_cotizacion} - {cliente_nombre}'
    
    def get_mensaje_whatsapp(self):
        cliente = self.cliente.nombre if self.cliente else "cliente"
        fecha = self.fecha_emision.strftime('%d/%m/%Y') if self.fecha_emision else ''
        numero = self.numero_cotizacion or ""
        total = f"${self.monto_total:,.0f}".replace(",", ".")

        return (
            f"Hola {cliente}, te enviamos tu cotización N°{numero} del {fecha} "
            f"por un total de {total}.\n\n"
            "Revisa el documento y contáctanos si deseas continuar con el servicio. ¡Gracias!"
        )


class ItemCotizacion(models.Model):
    """Modelo para items/líneas de una cotización"""
    
    cotizacion = models.ForeignKey(
        Cotizacion, 
        on_delete=models.CASCADE, 
        related_name='items',
        verbose_name="Cotización"
    )
    categoria = models.CharField(
        max_length=100, 
        default="Servicios", 
        blank=True,
        verbose_name="Categoría"
    )
    descripcion = models.CharField(
        max_length=300, 
        blank=True,
        verbose_name="Descripción"
    )
    cantidad = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=1, 
        validators=[MinValueValidator(0.01)],
        verbose_name="Cantidad"
    )
    precio_unitario = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0, 
        validators=[MinValueValidator(0)],
        verbose_name="Precio unitario"
    )
    
    class Meta:
        verbose_name = "Item de cotización"
        verbose_name_plural = "Items de cotización"
        ordering = ['id']
    
    @property
    def subtotal(self):
        """Calcula el subtotal del item (cantidad × precio)"""
        return self.cantidad * self.precio_unitario
    
    def __str__(self):
        return f"{self.descripcion} - ${self.precio_unitario}"


