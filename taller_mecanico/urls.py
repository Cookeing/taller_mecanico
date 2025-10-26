"""Rutas principales del proyecto."""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("admin/", admin.site.urls),
    path("clientes/", include("clientes.urls")),
    path("", lambda request: redirect("clientes:list")),
    path("vehiculos/", include("vehiculo.urls")),
    path("cotizaciones/", include("cotizaciones.urls")),
]
