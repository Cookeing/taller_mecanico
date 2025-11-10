from django.contrib import admin
from .models import Servicio, Documento, FotoServicio


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehiculo', 'fecha_servicio', 'estado', 'total')
    list_filter = ('estado', 'fecha_servicio')
    search_fields = ('vehiculo__patente', 'descripcion_trabajo')


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'servicio', 'tipo_documento', 'fecha_documento', 'monto')
    list_filter = ('tipo_documento', 'fecha_documento')


@admin.register(FotoServicio)
class FotoServicioAdmin(admin.ModelAdmin):
    list_display = ('id', 'servicio', 'descripcion', 'fecha_captura')
    list_filter = ('fecha_captura',)
    search_fields = ('servicio__vehiculo__patente', 'descripcion')
    readonly_fields = ('fecha_captura',)
