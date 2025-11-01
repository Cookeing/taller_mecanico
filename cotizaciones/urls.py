from django.urls import path
from . import views as v

app_name = "cotizaciones"

urlpatterns = [ 
    path("registrar/", v.RegistrarCotizacion, name="registrar_cotizacion"),
    path("historial/", v.historial_cotizaciones, name="listar_cotizaciones"),
    path("cliente/<int:cliente_id>/data/", v.get_cliente_data, name="cliente_data"),
]

