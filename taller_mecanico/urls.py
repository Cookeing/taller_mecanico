"""Rutas principales del proyecto."""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", views.home, name="home"),
    path("clientes/", include("clientes.urls")),
    path("vehiculos/", include("vehiculo.urls")),
    path("cotizaciones/", include("cotizaciones.urls")),
    path("", lambda request: redirect("clientes:list")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
