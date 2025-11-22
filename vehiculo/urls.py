from django.urls import path
from . import views

app_name = 'vehiculos'

urlpatterns = [
    path('', views.vehiculo_list, name='list'),
    path('crear/', views.vehiculo_create, name='crear'),
    path('<int:pk>/', views.vehiculo_detail, name='detail'),
    path('<int:pk>/editar/', views.vehiculo_update, name='update'),
    path('<int:pk>/borrar/', views.vehiculo_delete, name='delete'),
    path('api/buscar/', views.buscar_vehiculos_api, name='buscar_api'),
    path('api/buscar-por-cliente/<int:cliente_id>/', views.buscar_vehiculos_por_cliente_api, name='buscar_por_cliente_api'),
    path('inactivos/', views.vehiculos_inactivos, name='inactivos'),  # NUEVO
    path('<int:pk>/reactivar/', views.vehiculo_reactivar, name='reactivar'),  # NUEVO
]
