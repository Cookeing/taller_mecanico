# cotizaciones/context_processors.py

from django.conf import settings

def empresa_settings(request):
    return {
        'EMPRESA_NOMBRE': getattr(settings, 'EMPRESA_NOMBRE', ''),
        'EMPRESA_RUT': getattr(settings, 'EMPRESA_RUT', ''),
        'EMPRESA_GIRO': getattr(settings, 'EMPRESA_GIRO', ''),
        'EMPRESA_DIRECCION': getattr(settings, 'EMPRESA_DIRECCION', ''),
        'EMPRESA_TELEFONO': getattr(settings, 'EMPRESA_TELEFONO', ''),
        'EMPRESA_EMAIL': getattr(settings, 'EMPRESA_EMAIL', ''),
    }
