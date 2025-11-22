from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    """
    Vista principal del dashboard con estadísticas reales
    """
    
    # Importar modelos
    from clientes.models import Cliente
    from vehiculo.models import Vehiculo
    from servicios.models import Servicio
    from cotizaciones.models import Cotizacion
    
    # Estadísticas generales
    total_clientes = Cliente.objects.count()
    total_vehiculos = Vehiculo.objects.count()
    servicios_activos = Servicio.objects.filter(
        estado__in=['pendiente', 'proceso']
    ).count()
    cotizaciones_pendientes = Cotizacion.objects.filter(
        estado_cotizacion='PENDIENTE'
    ).count()
    
    # Servicios recientes (últimos 10)
    servicios_recientes = Servicio.objects.select_related(
        'vehiculo__cliente'
    ).order_by('-fecha_servicio')[:10]
    
    # Estadísticas financieras
    ingresos_totales = Servicio.objects.filter(
        estado='completado'
    ).aggregate(total=Sum('total'))['total'] or 0
    
    # Servicios del mes actual
    inicio_mes = timezone.now().replace(day=1, hour=0, minute=0, second=0)
    servicios_mes = Servicio.objects.filter(
        fecha_servicio__gte=inicio_mes
    ).count()
    
    # Cotizaciones aprobadas
    cotizaciones_aprobadas = Cotizacion.objects.filter(
        estado_cotizacion='APROBADA'
    ).count()
    
    context = {
        'total_clientes': total_clientes,
        'total_vehiculos': total_vehiculos,
        'servicios_activos': servicios_activos,
        'cotizaciones_pendientes': cotizaciones_pendientes,
        'servicios_recientes': servicios_recientes,
        'ingresos_totales': ingresos_totales,
        'servicios_mes': servicios_mes,
        'cotizaciones_aprobadas': cotizaciones_aprobadas,
    }
    
    return render(request, 'home.html', context)