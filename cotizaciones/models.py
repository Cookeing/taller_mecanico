from django.db import models

#modelos de otras apps
from clientes.models import Cliente
from vehiculo.models import Vehiculo

# Create your models here.


class Cotizacion(models.Model):
    estado_cotizacion_choices = [
        ('PENDIENTE', 'Pendiente'),
        ('APROBADA', 'Aprobada'),
        ('RECHAZADA', 'Rechazada'),
    ]

    numero_cotizacion =models.CharField(max_length=20, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)    
    descripcion= models.CharField(max_length=300, help_text="Descripción breve del trabajo a realizar")
    monto_total =models.IntegerField()
    estado_cotizacion = models.CharField(max_length=10, choices=estado_cotizacion_choices, default='PENDIENTE')
    #Relaciones 
    cliente= models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='cotizaciones')
    vehiculo= models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='cotizaciones')
    #futura implementacion de items como documentos

    
    def __str__(self):
        return f'Cotización {self.numero_cotizacion} - {self.cliente.nombre}'
    