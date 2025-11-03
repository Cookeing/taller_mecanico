from django.urls import path
from vehiculo import views as v

app_name = "vehiculos"

urlpatterns = [
    path("", v.vehiculo_list, name="list"),
    path("api/buscar/", v.buscar_vehiculos_api, name="api_buscar"),
    path("api/buscar-por-cliente/", v.buscar_vehiculos_por_cliente_api, name="api_buscar_por_cliente"), 
    path("nuevo/", v.vehiculo_create, name="crear"),
    path("<int:pk>/editar/", v.vehiculo_update, name="editar"),
    path("<int:pk>/borrar/", v.vehiculo_delete, name="eliminar"),
    path("<int:pk>/", v.vehiculo_detail, name="detalles"),
    path('servicios/', v.servicio_list, name='servicio_list'),
    path('servicios/nuevo/', v.servicio_create, name='servicio_create'),
    path('servicios/<int:pk>/editar/', v.servicio_update, name='servicio_update'),
    path('servicios/<int:pk>/cotizaciones/', v.servicio_cotizaciones, name='servicio_cotizaciones'),
]
