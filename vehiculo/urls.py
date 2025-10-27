from django.urls import path
from . import views

app_name = "vehiculos"

urlpatterns = [
    path("", views.vehiculo_list, name="list"),
    path("api/buscar/", views.buscar_vehiculos_api, name="api_buscar"),
    path("api/buscar-por-cliente/", views.buscar_vehiculos_por_cliente_api, name="api_buscar_por_cliente"), 
    path("nuevo/", views.vehiculo_create, name="create"),
    path("<int:pk>/editar/", views.vehiculo_update, name="edit"),
    path("<int:pk>/borrar/", views.vehiculo_delete, name="delete"),
    path("<int:pk>/", views.vehiculo_detail, name="detail"),
    path('servicios/', views.servicio_list, name='servicio_list'),
    path('servicios/nuevo/', views.servicio_create, name='servicio_create'),
    path('servicios/<int:pk>/editar/', views.servicio_update, name='servicio_update'),

]
