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
    
    # Estadísticas generales (solo registros activos)
    total_clientes = Cliente.objects.filter(activo=True).count()
    total_vehiculos = Vehiculo.objects.filter(activo=True).count()
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
    
    # Ingresos del mes actual
    ingresos_mes = Servicio.objects.filter(
        fecha_servicio__gte=inicio_mes,
        estado='completado'
    ).aggregate(total=Sum('total'))['total'] or 0
    
    # Cotizaciones aprobadas con su valor total
    cotizaciones_aprobadas = Cotizacion.objects.filter(
        estado_cotizacion='APROBADA'
    ).count()
    
    valor_cotizaciones_aprobadas = Cotizacion.objects.filter(
        estado_cotizacion='APROBADA'
    ).aggregate(total=Sum('monto_total'))['total'] or 0
    
    # Cotizaciones pendientes con su valor potencial
    valor_cotizaciones_pendientes = Cotizacion.objects.filter(
        estado_cotizacion='PENDIENTE'
    ).aggregate(total=Sum('monto_total'))['total'] or 0
    
    context = {
        'total_clientes': total_clientes,
        'total_vehiculos': total_vehiculos,
        'servicios_activos': servicios_activos,
        'cotizaciones_pendientes': cotizaciones_pendientes,
        'servicios_recientes': servicios_recientes,
        'ingresos_totales': ingresos_totales,
        'servicios_mes': servicios_mes,
        'ingresos_mes': ingresos_mes,
        'cotizaciones_aprobadas': cotizaciones_aprobadas,
        'valor_cotizaciones_aprobadas': valor_cotizaciones_aprobadas,
        'valor_cotizaciones_pendientes': valor_cotizaciones_pendientes,
    }
    
    return render(request, 'home.html', context)