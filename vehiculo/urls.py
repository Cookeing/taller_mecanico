from django.urls import path
from vehiculo import views as v

app_name = 'vehiculos'

urlpatterns = [
    # Vehículos
    path('', v.vehiculo_list, name='list'),
    path('nuevo/', v.vehiculo_create, name='crear'),
    path('<int:pk>/editar/', v.vehiculo_update, name='update'),
    path('<int:pk>/eliminar/', v.vehiculo_delete, name='delete'),
    path('<int:pk>/', v.vehiculo_detail, name='detail'),

    
    

    # Búsquedas
    path('api/buscar/', v.buscar_vehiculos_api, name='buscar_api'),
    path('api/cliente/<int:cliente_id>/', v.buscar_vehiculos_por_cliente_api, name='buscar_por_cliente_api'),
]
