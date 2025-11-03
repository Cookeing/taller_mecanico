from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, render, redirect
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET
from django.utils import timezone
from datetime import timedelta
import json

from vehiculo.models import Servicio
from .models import Cotizacion, ItemCotizacion
from .forms import CotizacionForm
from clientes.models import Cliente
from .utils import generar_pdf_cotizacion


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
    cotizaciones = Cotizacion.objects.all().select_related('cliente', 'servicio').order_by('-fecha_creacion')

    cliente = request.GET.get('cliente')
    estado = request.GET.get('estado')

    if cliente:
        cotizaciones = cotizaciones.filter(cliente__nombre__icontains=cliente)
    if estado:
        cotizaciones = cotizaciones.filter(estado_cotizacion=estado)

    # Estadísticas para las tarjetas
    cotizaciones_aprobadas = Cotizacion.objects.filter(estado_cotizacion='APROBADA').count()
    cotizaciones_pendientes = Cotizacion.objects.filter(estado_cotizacion='PENDIENTE').count()

    # Paginación
    paginator = Paginator(cotizaciones, 10)  # 10 items por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'cotizaciones/cotizacion_list.html', {
        'cotizaciones': page_obj,
        'page_obj': page_obj,
        'is_paginated': paginator.num_pages > 1,
        'cotizaciones_aprobadas': cotizaciones_aprobadas,
        'cotizaciones_pendientes': cotizaciones_pendientes,
    })

# def historial_cotizaciones(request):
#     # CORREGIDO: Eliminado 'vehiculo' del select_related
#     cotizaciones = Cotizacion.objects.all().select_related('cliente')

#     cliente = request.GET.get('cliente')
#     # CORREGIDO: Eliminado el filtro por patente
#     # patente = request.GET.get('patente')

#     if cliente:
#         cotizaciones = cotizaciones.filter(cliente__nombre__icontains=cliente)
#     # CORREGIDO: Eliminado el filtro por vehículo
#     # if patente:
#     #    cotizaciones = cotizaciones.filter(vehiculo__patente__icontains=patente)

#     return render(request, 'cotizaciones/cotizacion_list.html', {
#         'cotizaciones': cotizaciones
#     })

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

def EditarCotizacion(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    servicio = cotizacion.servicio
    
    if request.method == "POST":
        form = CotizacionForm(request.POST, instance=cotizacion)
        
        if form.is_valid(): 
            cotizacion = form.save(commit=False)
            
            # Procesar items (igual que en RegistrarCotizacion)
            items_data_json = request.POST.get('items_data', '[]')
            try:
                items_data = json.loads(items_data_json)
            except json.JSONDecodeError:
                items_data = []
                messages.error(request, "Error en los datos de los items.")
                return render(request, "cotizaciones/cotizacion_form.html", {
                    "form": form,
                    "clientes": Cliente.objects.all(),
                    "servicio": servicio,
                })
            
            # Eliminar items existentes y crear nuevos
            cotizacion.items.all().delete()
            
            subtotal = 0
            for item_data in items_data:
                cantidad = float(item_data.get('cantidad', 0))
                precio_unitario = float(item_data.get('precio_unitario', 0))
                subtotal += cantidad * precio_unitario
                
                ItemCotizacion.objects.create(
                    cotizacion=cotizacion,
                    categoria=item_data.get('categoria', 'Servicios'),
                    descripcion=item_data.get('descripcion', ''),
                    cantidad=cantidad,
                    precio_unitario=precio_unitario
                )
            
            # Actualizar totales
            cotizacion.subtotal = subtotal
            cotizacion.save()
            
            messages.success(request, "Cotización actualizada exitosamente.")    
            return redirect("cotizaciones:listar_cotizaciones")
        else:
            messages.error(request, "Error al actualizar la cotización.") 
    else:
        form = CotizacionForm(instance=cotizacion)
    
    clientes = Cliente.objects.all()
    
    return render(request, "cotizaciones/cotizacion_form.html", {
        "form": form,
        "clientes": clientes,
        "servicio": servicio,
    })

# Vista para duplicar cotización
def DuplicarCotizacion(request, pk):
    cotizacion_original = get_object_or_404(Cotizacion, pk=pk)
    
    if request.method == "POST":
        form = CotizacionForm(request.POST)
        
        if form.is_valid(): 
            nueva_cotizacion = form.save(commit=False)
            nueva_cotizacion.numero_cotizacion = ''  # Para generar nuevo número
            nueva_cotizacion.estado_cotizacion = 'PENDIENTE'
            nueva_cotizacion.save()
            
            # Copiar items
            for item in cotizacion_original.items.all():
                ItemCotizacion.objects.create(
                    cotizacion=nueva_cotizacion,
                    categoria=item.categoria,
                    descripcion=item.descripcion,
                    cantidad=item.cantidad,
                    precio_unitario=item.precio_unitario
                )
            
            messages.success(request, "Cotización duplicada exitosamente.")    
            return redirect("cotizaciones:listar_cotizaciones")
    else:
        # Pre-cargar datos de la cotización original
        initial_data = {
            'empresa_nombre': cotizacion_original.empresa_nombre,
            'empresa_rut': cotizacion_original.empresa_rut,
            'empresa_giro': cotizacion_original.empresa_giro,
            'empresa_direccion': cotizacion_original.empresa_direccion,
            'empresa_telefono': cotizacion_original.empresa_telefono,
            'empresa_email': cotizacion_original.empresa_email,
            'fecha_emision': timezone.now().date(),
            'fecha_validez': (timezone.now() + timedelta(days=30)).date(),
            'cliente': cotizacion_original.cliente,
            'forma_pago': cotizacion_original.forma_pago,
            'plazo_pago': cotizacion_original.plazo_pago,
        }
        form = CotizacionForm(initial=initial_data)
    
    clientes = Cliente.objects.all()
    
    return render(request, "cotizaciones/cotizacion_form.html", {
        "form": form,
        "clientes": clientes,
        "servicio": cotizacion_original.servicio,
    })
    
def EliminarCotizacion(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    
    if request.method == "POST":
        numero_cotizacion = cotizacion.numero_cotizacion
        cotizacion.delete()
        messages.success(request, f"Cotización {numero_cotizacion} eliminada exitosamente.")
        return redirect("cotizaciones:listar_cotizaciones")
    
    return redirect("cotizaciones:listar_cotizaciones")

def VerPDF(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    # Por ahora redirige a la vista de edición
    # Más adelante puedes implementar la generación de PDF
    messages.info(request, "Funcionalidad de PDF en desarrollo.")
    return redirect("cotizaciones:editar_cotizacion", pk=pk)
#$$ esta vista dara al boton de ver el historial la posibilidad de descargar y poder generar el pdf que se creo en utlis.py
def descargar_pdf_cotizacion(request, cotizacion_id):
    
#   se se recoje el id de cliente en el formulario de cotizacion y verifica si exite comparandolo con la bs 
    cotizacion = get_object_or_404(
        Cotizacion.objects.select_related('cliente', 'servicio__vehiculo').prefetch_related('items'),
        id=cotizacion_id
    )
    
    buffer = generar_pdf_cotizacion(cotizacion)
    
    # Preparar respuesta HTTP con el pdf generado por la funcion de utils o le buffer  
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="cotizacion_{cotizacion.numero_cotizacion}.pdf"'
    response.write(buffer.getvalue())
    
    return response
