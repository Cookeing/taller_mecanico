from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.utils import timezone
from datetime import timedelta
import json

from vehiculo.models import Servicio
from .models import Cotizacion, ItemCotizacion
from .forms import CotizacionForm
from clientes.models import Cliente



def RegistrarCotizacion(request):
    # NUEVO: Obtener servicio_id sin afectar lógica existente
    servicio_id = request.GET.get('servicio_id') or request.POST.get('servicio_id')
    servicio = None
    
    if servicio_id:
        try:
            servicio = Servicio.objects.select_related('vehiculo__cliente').get(id=servicio_id)
        except Servicio.DoesNotExist:
            # No mostrar error para no interrumpir flujo existente
            pass
    
    if request.method == "POST":
        form = CotizacionForm(request.POST)
        
        if form.is_valid(): 
            cotizacion = form.save(commit=False)
            
            # NUEVO: Asignar servicio si existe (sin afectar lógica existente)
            if servicio:
                cotizacion.servicio = servicio
                # Opcional: asignar cliente automáticamente si no está seleccionado
                if not cotizacion.cliente and servicio.vehiculo and servicio.vehiculo.cliente:
                    cotizacion.cliente = servicio.vehiculo.cliente
            
            # MANTENER TODA LA LÓGICA EXISTENTE SIN CAMBIOS
            items_data_json = request.POST.get('items_data', '[]')
            try:
                items_data = json.loads(items_data_json)
            except json.JSONDecodeError:
                items_data = []
                messages.error(request, "Error en los datos de los items.")
                return render(request, "cotizaciones/cotizacion_form.html", {
                    "form": form,
                    "clientes": Cliente.objects.all(),
                    "servicio": servicio,  # NUEVO: pasar servicio al template
                })
            
            subtotal = 0
            for item_data in items_data:
                cantidad = float(item_data.get('cantidad', 0))
                precio_unitario = float(item_data.get('precio_unitario', 0))
                subtotal += cantidad * precio_unitario
            
            # Mantener lógica existente
            cotizacion.subtotal = subtotal
            cotizacion.save()
            
            # Mantener lógica existente
            for item_data in items_data:
                ItemCotizacion.objects.create(
                    cotizacion=cotizacion,
                    categoria=item_data.get('categoria', 'Servicios'),
                    descripcion=item_data.get('descripcion', ''),
                    cantidad=item_data.get('cantidad', 0),
                    precio_unitario=item_data.get('precio_unitario', 0)
                )
            
            messages.success(request, "Cotización registrada exitosamente.")    
            return redirect("cotizaciones:listar_cotizaciones")
        else:
            messages.error(request, "Error al registrar la cotización.") 
    else:
        # MANTENER LÓGICA EXISTENTE
        initial_data = {
            'fecha_emision': timezone.now().date(),
            'fecha_validez': (timezone.now() + timedelta(days=30)).date(),
        }
        
        # NUEVO: Pre-cargar cliente si hay servicio (sin afectar lógica existente)
        if servicio and servicio.vehiculo and servicio.vehiculo.cliente:
            initial_data['cliente'] = servicio.vehiculo.cliente
        
        form = CotizacionForm(initial=initial_data)
    
    clientes = Cliente.objects.all()
    
    return render(request, "cotizaciones/cotizacion_form.html", {
        "form": form,
        "clientes": clientes,
        "servicio": servicio,  # NUEVO: pasar servicio al template
    })

def historial_cotizaciones(request):
    # CORREGIDO: Eliminado 'vehiculo' del select_related
    cotizaciones = Cotizacion.objects.all().select_related('cliente')

    cliente = request.GET.get('cliente')
    # CORREGIDO: Eliminado el filtro por patente
    # patente = request.GET.get('patente')

    if cliente:
        cotizaciones = cotizaciones.filter(cliente__nombre__icontains=cliente)
    # CORREGIDO: Eliminado el filtro por vehículo
    # if patente:
    #    cotizaciones = cotizaciones.filter(vehiculo__patente__icontains=patente)

    return render(request, 'cotizaciones/cotizacion_list.html', {
        'cotizaciones': cotizaciones
    })

# APIs para autorelleno (mantener solo la de cliente)
@require_GET
def get_cliente_data(request, cliente_id):
    """API para obtener datos del cliente"""
    try:
        cliente = Cliente.objects.get(id=cliente_id)
        data = {
            'nombre': cliente.nombre,
            'rut': cliente.rut or '',
            'telefono': cliente.telefono or '',
            'direccion': cliente.direccion or '',
            'email': cliente.email or '',
            'contacto': cliente.contacto or '',
        }
        return JsonResponse(data)
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente no encontrado'}, status=404)

# CORREGIDO: Esta función ya no es necesaria, puedes eliminarla o comentarla
# @require_GET
# def get_vehiculos_by_cliente(request, cliente_id):
#     """API para obtener vehículos de un cliente"""
#     vehiculos = Vehiculo.objects.filter(cliente_id=cliente_id).values('id', 'patente', 'marca', 'modelo')
#     return JsonResponse(list(vehiculos), safe=False)