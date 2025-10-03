"""Rutas del módulo Clientes."""

from django.urls import path
from . import views

app_name = "clientes"

urlpatterns = [
    path("", views.cliente_list, name="list"),
    path("buscar/", views.cliente_list, name="buscar"),  # soporte con ?q=
    path("api/buscar/", views.buscar_clientes_api, name="api_buscar"),  # endpoint JSON para live search
    path("nuevo/", views.cliente_create, name="create"),
    path("<int:pk>/editar/", views.cliente_update, name="update"),
    path("<int:pk>/borrar/", views.cliente_delete, name="delete"),
]
