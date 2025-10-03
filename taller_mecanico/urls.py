"""Rutas principales del proyecto."""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


urlpatterns = [
    path("admin/", admin.site.urls),
    path("clientes/", include("clientes.urls")),
    path("", lambda request: redirect("clientes:list")),  # 👈 redirige al listado de clientes
]
