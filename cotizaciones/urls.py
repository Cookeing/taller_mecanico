from django.urls import path
from . import views as v

app_name = "cotizaciones"

urlpatterns = [ 
    path("registrar/", v.RegistrarCotizacion, name="registrar_cotizacion"),
    path('editar/<int:pk>/', v.EditarCotizacion, name='editar_cotizacion'),
    path('eliminar/<int:pk>/', v.EliminarCotizacion, name='eliminar_cotizacion'),
    path('duplicar/<int:pk>/', v.DuplicarCotizacion, name='duplicar_cotizacion'),
    path("historial/", v.historial_cotizaciones, name="listar_cotizaciones"),
    path("cliente/<int:cliente_id>/data/", v.get_cliente_data, name="cliente_data"),
    path('pdf/<int:pk>/', v.VerPDF, name='ver_pdf'),
    path('listar/', v.historial_cotizaciones, name='listar_cotizaciones'),
    #nueva ruta qu e genera el pdf eliminaren proximas v solo uso para testeo 
    path("pdf/<int:cotizacion_id>/", v.descargar_pdf_cotizacion, name="descargar_pdf"),
    path("email/<int:cotizacion_id>/", v.enviar_cotizacion_email, name="enviar_email"),
]
