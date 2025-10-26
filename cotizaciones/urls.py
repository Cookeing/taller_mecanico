from django.urls import path
from . import views as v


urlpatterns = [ 
    path("Registrar/", v.RegistrarCotizacion, name="registrar_cotizacion"),
    path('historial/', v.historial_cotizaciones, name='historial_cotizaciones'),
]
