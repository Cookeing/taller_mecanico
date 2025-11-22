from django.urls import path
from servicios import views as v

app_name = 'servicios'

urlpatterns = [
    path('', v.servicio_list, name='list'),
    path('nuevo/', v.servicio_create, name='create'),
    path('<int:pk>/editar/', v.servicio_update, name='update'),
    path('<int:pk>/eliminar/', v.servicio_delete, name='delete'),
    path('<int:pk>/cambiar_estado/', v.cambiar_estado_servicio, name='cambiar_estado'),
    
    # Documentos
    path('<int:servicio_id>/documentos/', v.documentos_servicio, name='documentos_servicio'),
    path('<int:servicio_id>/documentos/nuevo/', v.documento_upload, name='documento_upload'),
    path('documentos/<int:pk>/eliminar/', v.documento_delete, name='documento_delete'),
    path('<int:servicio_id>/documentos/', v.documentos_servicio, name='documentos_servicio'),

    
    # Fotos
    path('<int:servicio_id>/fotos/', v.fotos_servicio, name='fotos_servicio'),
    path('fotos/<int:pk>/eliminar/', v.foto_delete, name='foto_delete'),
]