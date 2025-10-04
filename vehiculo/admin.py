from django.contrib import admin
from vehiculo.models import Vehiculo

# Register your models here.
@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ("patente", "cliente", "marca", "modelo", "anio")
    search_fields = ("patente", "cliente__nombre", "cliente__rut")