"""Rutas principales del proyecto."""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", views.home, name="home"),
    path("clientes/", include("clientes.urls")),
    path("vehiculos/", include("vehiculo.urls")),
    path("cotizaciones/", include("cotizaciones.urls")),
    path("", lambda request: redirect("clientes:list")),
]
