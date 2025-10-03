"""Configuración del admin para Clientes."""

from django.contrib import admin
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    """Opciones de listado y búsqueda en el panel admin."""
    list_display = ("nombre", "rut", "telefono", "direccion")
    search_fields = ("nombre", "rut", "telefono")
