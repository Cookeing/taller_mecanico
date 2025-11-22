from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.cliente_list, name='list'),
    path('crear/', views.cliente_create, name='create'),
    path('<int:pk>/editar/', views.cliente_update, name='update'),
    path('<int:pk>/borrar/', views.cliente_delete, name='delete'),
    path('api/buscar/', views.buscar_clientes_api, name='api_buscar'),
    path('inactivos/', views.clientes_inactivos, name='inactivos'),  # NUEVO
    path('<int:pk>/reactivar/', views.cliente_reactivar, name='reactivar'),  # NUEVO
]
