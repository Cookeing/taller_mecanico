from django.urls import path
from . import views

app_name = 'vehiculos'

urlpatterns = [
    # Vehículos
    path('', views.vehiculo_list, name='list'),
    path('nuevo/', views.vehiculo_create, name='create'),
    path('<int:pk>/editar/', views.vehiculo_update, name='update'),
    path('<int:pk>/eliminar/', views.vehiculo_delete, name='delete'),
    path('<int:pk>/', views.vehiculo_detail, name='detail'),

    # Documentos
    path('servicios/<int:servicio_id>/documentos/', views.documentos_servicio, name='documentos_servicio'),
    path('servicios/<int:servicio_id>/documentos/nuevo/', views.documento_upload, name='documento_upload'),
    path('documentos/<int:pk>/eliminar/', views.documento_delete, name='documento_delete'),

    # Búsquedas
    path('api/buscar/', views.buscar_vehiculos_api, name='buscar_api'),
    path('api/cliente/<int:cliente_id>/', views.buscar_vehiculos_por_cliente_api, name='buscar_por_cliente_api'),
]
