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
]

