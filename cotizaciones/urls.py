from django.urls import path
from . import views as v

app_name = "cotizaciones"

urlpatterns = [ 
    path("registrar/", v.RegistrarCotizacion, name="registrar_cotizacion"),
    path("historial/", v.historial_cotizaciones, name="listar_cotizaciones"),
    path("cliente/<int:cliente_id>/data/", v.get_cliente_data, name="cliente_data"),
    #nueva ruta qu e genera el pdf eliminaren proximas v solo uso para testeo 
    path("pdf/<int:cotizacion_id>/", v.descargar_pdf_cotizacion, name="descargar_pdf"),
]

