
from django.db import models
from django.core.validators import MinValueValidator
from clientes.models import Cliente
from servicios.models import Servicio
from django.utils import timezone
from urllib.parse import quote
from decimal import Decimal


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

    empresa_nombre = models.CharField(max_length=200, blank=True)
    empresa_rut = models.CharField(max_length=20, blank=True)
    empresa_giro = models.CharField(max_length=200, blank=True)
    empresa_direccion = models.TextField(blank=True)
    empresa_telefono = models.CharField(max_length=20, blank=True)
    empresa_email = models.EmailField(blank=True)
    empresa_sitio_web = models.URLField(blank=True, null=True)
    empresa_contacto_persona = models.CharField(max_length=100, blank=True)
    logo = models.ImageField(upload_to='cotizaciones/logos/', blank=True, null=True)

    numero_cotizacion = models.CharField(max_length=20, unique=True, blank=True)
    fecha_emision = models.DateField(default=timezone.now)
    fecha_validez = models.DateField(blank=True, null=True)

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='cotizaciones',
                                blank=True, null=True)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='cotizaciones',
                                 blank=True, null=True)

    forma_pago = models.CharField(max_length=20, choices=FORMA_PAGO_CHOICES, blank=True)
    plazo_pago = models.CharField(max_length=10, choices=PLAZO_PAGO_CHOICES, blank=True)

    notas_adicionales = models.TextField(blank=True)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))
    iva = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))
    monto_total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"))

    estado_cotizacion = models.CharField(max_length=10, choices=ESTADO_COTIZACION_CHOICES,
                                         default='PENDIENTE')

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def generar_numero_cotizacion(self):
        ultima = Cotizacion.objects.order_by('-id').first()
        if ultima and ultima.numero_cotizacion:
            try:
                nuevo = int(ultima.numero_cotizacion) + 1
            except:
                nuevo = 1
        else:
            nuevo = 1
        return str(nuevo).zfill(4)

    def save(self, *args, **kwargs):
        if not self.numero_cotizacion:
            self.numero_cotizacion = self.generar_numero_cotizacion()

        # Usar Decimal seguro
        subtotal_decimal = Decimal(str(self.subtotal)) if self.subtotal else Decimal("0.00")
        self.iva = subtotal_decimal * Decimal("0.19")
        self.monto_total = subtotal_decimal + self.iva

        try:
            super().save(*args, **kwargs)
        except Exception as e:
            if 'duplicate' in str(e).lower() or '1062' in str(e):
                self.numero_cotizacion = self.generar_numero_cotizacion()
                super().save(*args, **kwargs)
            else:
                raise e
        except Exception as e:
            if 'duplicate' in str(e).lower() or '1062' in str(e):
                self.numero_cotizacion = self.generar_numero_cotizacion()
                super().save(*args, **kwargs)
            else:
                raise e

    def __str__(self):
        return f'Cotización {self.numero_cotizacion} - {self.cliente.nombre if self.cliente else "Sin cliente"}'

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
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name='items')
    categoria = models.CharField(max_length=100, default="Servicios", blank=True)
    descripcion = models.CharField(max_length=300, blank=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("1.00"),
                                   validators=[MinValueValidator(Decimal("0.01"))])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"),
                                          validators=[MinValueValidator(Decimal("0.00"))])

    class Meta:
        ordering = ['id']

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.descripcion} - ${self.precio_unitario}"
