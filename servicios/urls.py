from django.urls import path
from . import views

app_name = 'servicios'

urlpatterns = [
    path('', views.servicio_list, name='list'),
    path('nuevo/', views.servicio_create, name='create'),
    path('<int:pk>/editar/', views.servicio_update, name='update'),
    path('<int:pk>/eliminar/', views.servicio_delete, name='delete'),
    path('<int:pk>/cambiar_estado/', views.cambiar_estado_servicio, name='cambiar_estado'),
]
