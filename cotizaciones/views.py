from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET
from django.utils import timezone
from datetime import timedelta
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

from servicios.models import Servicio
from .models import Cotizacion, ItemCotizacion
from .forms import CotizacionForm
from clientes.models import Cliente
from .utils import generar_pdf_cotizacion
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


def RegistrarCotizacion(request):
    # Obtener servicio_id
    servicio_id = request.GET.get('servicio_id') or request.POST.get('servicio_id')
    servicio = None
    
    if servicio_id:
        try:
            servicio = Servicio.objects.select_related('vehiculo__cliente').get(id=servicio_id)
        except Servicio.DoesNotExist:
            pass
    
    if request.method == "POST":
        form = CotizacionForm(request.POST, request.FILES)
        
        # DEBUG: Mostrar errores del formulario
        if not form.is_valid():
            print("FORM ERRORS (cotizacion):", form.errors)
            messages.error(request, "Error al registrar la cotización. Por favor revise los campos marcados.")
            
            # Pasar fechas para rellenar
            return render(request, "cotizaciones/cotizacion_form.html", {
                "form": form,
                "clientes": Cliente.objects.all(),
                "servicio": servicio,
                "today": timezone.now().date(),
                "validez": (timezone.now() + timedelta(days=30)).date(),
            })
        
        # Si es válido, procesar
        cotizacion = form.save(commit=False)
        
        # Asignar servicio si existe
        if servicio:
            cotizacion.servicio = servicio
            if not cotizacion.cliente and servicio.vehiculo and servicio.vehiculo.cliente:
                cotizacion.cliente = servicio.vehiculo.cliente
        
        # Procesar items
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
                "today": timezone.now().date(),
                "validez": (timezone.now() + timedelta(days=30)).date(),
            })
        
        # Calcular subtotal
        subtotal = 0
        for item_data in items_data:
            cantidad = float(item_data.get('cantidad', 0))
            precio_unitario = float(item_data.get('precio_unitario', 0))
            subtotal += cantidad * precio_unitario
        
        cotizacion.subtotal = subtotal
        cotizacion.save()
        if cotizacion.servicio:
            cotizacion.servicio.actualizar_total()

        
        # Crear items
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
        # GET: Pre-cargar datos
        initial_data = {
            'fecha_emision': timezone.now().date(),
            'fecha_validez': (timezone.now() + timedelta(days=30)).date(),
            'estado_cotizacion': 'PENDIENTE',
        }
        
        # Pre-cargar cliente si hay servicio
        if servicio and servicio.vehiculo and servicio.vehiculo.cliente:
            initial_data['cliente'] = servicio.vehiculo.cliente
        
        form = CotizacionForm(initial=initial_data)
    
    clientes = Cliente.objects.all()
    
    return render(request, "cotizaciones/cotizacion_form.html", {
        "form": form,
        "clientes": clientes,
        "servicio": servicio,
        "today": timezone.now().date(),
        "validez": (timezone.now() + timedelta(days=30)).date(),
    })


def historial_cotizaciones(request):
    cotizaciones = Cotizacion.objects.all().select_related('cliente', 'servicio').order_by('-fecha_creacion')

    cliente = request.GET.get('cliente')
    estado = request.GET.get('estado')

    if cliente:
        cotizaciones = cotizaciones.filter(cliente__nombre__icontains=cliente)
    if estado:
        cotizaciones = cotizaciones.filter(estado_cotizacion=estado)

    # Estadísticas
    cotizaciones_aprobadas = Cotizacion.objects.filter(estado_cotizacion='APROBADA').count()
    cotizaciones_pendientes = Cotizacion.objects.filter(estado_cotizacion='PENDIENTE').count()

    # Paginación
    paginator = Paginator(cotizaciones, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'cotizaciones/cotizacion_list.html', {
        'cotizaciones': page_obj,
        'page_obj': page_obj,
        'is_paginated': paginator.num_pages > 1,
        'cotizaciones_aprobadas': cotizaciones_aprobadas,
        'cotizaciones_pendientes': cotizaciones_pendientes,
    })


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


def EditarCotizacion(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    servicio = cotizacion.servicio
    items = cotizacion.items.all()
    
    if request.method == 'POST':
        form = CotizacionForm(request.POST, request.FILES, instance=cotizacion)
        
        if not form.is_valid():
            print("FORM ERRORS (editar):", form.errors)
            messages.error(request, 'Error al actualizar la cotización. Por favor revise los campos.')
            return render(request, 'cotizaciones/cotizacion_form.html', {
                'form': form,
                'cotizacion': cotizacion,
                'items': items,
                'is_edit': True,
                'servicio': servicio,
                "today": timezone.now().date(),
                "validez": (timezone.now() + timedelta(days=30)).date(),
            })
        
        cotizacion = form.save(commit=False)
        
        # ✅ Reasignar servicio si viene vacío del formulario
        if not cotizacion.servicio:
            cotizacion.servicio = servicio
        
        items_data_json = request.POST.get('items_data', '[]')
        try:
            items_data = json.loads(items_data_json)
        except json.JSONDecodeError:
            items_data = []
            messages.error(request, "Error en los datos de los items.")
            return render(request, 'cotizaciones/cotizacion_form.html', {
                'form': form,
                'cotizacion': cotizacion,
                'items': items,
                'is_edit': True,
                'servicio': servicio,
                "today": timezone.now().date(),
                "validez": (timezone.now() + timedelta(days=30)).date(),
            })
        
        # Eliminar items existentes
        cotizacion.items.all().delete()
        
        # Crear nuevos items
        subtotal = 0
        for item_data in items_data:
            cantidad = float(item_data.get('cantidad', 0))
            precio_unitario = float(item_data.get('precio_unitario', 0))
            subtotal += (cantidad * precio_unitario)
            
            ItemCotizacion.objects.create(
                cotizacion=cotizacion,
                categoria=item_data.get('categoria', 'Servicios'),
                descripcion=item_data.get('descripcion', ''),
                cantidad=cantidad,
                precio_unitario=precio_unitario
            )
        
        cotizacion.subtotal = subtotal
        cotizacion.save()
        # AGREGADO: Actualizar total del servicio
        if cotizacion.servicio:
            cotizacion.servicio.actualizar_total()

        
        messages.success(request, 'Cotización actualizada exitosamente.')
        return redirect('cotizaciones:listar_cotizaciones')
    
    else:
        form = CotizacionForm(instance=cotizacion)
    
    return render(request, 'cotizaciones/cotizacion_form.html', {
        'form': form,
        'cotizacion': cotizacion,
        'items': items,
        'is_edit': True,
        'servicio': servicio,
        "today": timezone.now().date(),
        "validez": (timezone.now() + timedelta(days=30)).date(),
    })

    
def DuplicarCotizacion(request, pk):
    cotizacion_original = get_object_or_404(Cotizacion, pk=pk)
    
    if request.method == "POST":
        form = CotizacionForm(request.POST)
        
        if form.is_valid(): 
            nueva_cotizacion = form.save(commit=False)
            nueva_cotizacion.numero_cotizacion = ''
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
        "today": timezone.now().date(),
        "validez": (timezone.now() + timedelta(days=30)).date(),
    })

    
def EliminarCotizacion(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    
    if request.method == "POST":
        numero_cotizacion = cotizacion.numero_cotizacion
        servicio = cotizacion.servicio  # <<< guardar servicio antes de borrar
        cotizacion.delete()

        if servicio:
            servicio.actualizar_total()  # <<< AÑADIR ESTA LÍNEA

        messages.success(request, f"Cotización {numero_cotizacion} eliminada exitosamente.")
        return redirect("cotizaciones:listar_cotizaciones")
    
    return redirect("cotizaciones:listar_cotizaciones")



def VerPDF(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    messages.info(request, "Funcionalidad de PDF en desarrollo.")
    return redirect("cotizaciones:editar_cotizacion", pk=pk)


def descargar_pdf_cotizacion(request, cotizacion_id):
    cotizacion = get_object_or_404(
        Cotizacion.objects.select_related('cliente', 'servicio__vehiculo').prefetch_related('items'),
        id=cotizacion_id
    )
    
    buffer = generar_pdf_cotizacion(cotizacion)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="cotizacion_{cotizacion.numero_cotizacion}.pdf"'
    response.write(buffer.getvalue())
    
    return response


def enviar_cotizacion_email(request, cotizacion_id):
    """Vista para enviar cotización por email con PDF adjunto"""
    cotizacion = get_object_or_404(
        Cotizacion.objects.select_related('cliente', 'servicio__vehiculo').prefetch_related('items'),
        id=cotizacion_id
    )
    
    if not cotizacion.cliente or not cotizacion.cliente.email:
        messages.error(request, "El cliente no tiene un email registrado.")
        return redirect('cotizaciones:listar_cotizaciones')
    
    try:
        buffer = generar_pdf_cotizacion(cotizacion)
        
        html_content = render_to_string('cotizaciones/email_cotizacion.html', {
            'cotizacion': cotizacion,
        })
        
        asunto = f"Cotización N° {cotizacion.numero_cotizacion} - {cotizacion.empresa_nombre or 'Taller Mecánico'}"
        
        email = EmailMessage(
            subject=asunto,
            body=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER,
            to=[cotizacion.cliente.email],
        )
        
        email.content_subtype = "html"
        
        email.attach(
            f'cotizacion_{cotizacion.numero_cotizacion}.pdf',
            buffer.getvalue(),
            'application/pdf'
        )
        
        email.send(fail_silently=False)
        
        messages.success(
            request, 
            f"Cotización enviada exitosamente a {cotizacion.cliente.email}"
        )
        
    except Exception as e:
        messages.error(
            request, 
            f"Error al enviar el email: {str(e)}"
        )
    
    return redirect('cotizaciones:listar_cotizaciones')

@csrf_exempt
@require_POST
def cambiar_estado_cotizacion(request, cotizacion_id):
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)
    nuevo_estado = request.POST.get("nuevo_estado")

    if nuevo_estado in dict(Cotizacion.ESTADO_COTIZACION_CHOICES):
        cotizacion.estado_cotizacion = nuevo_estado
        cotizacion.save()
        if cotizacion.servicio:
            cotizacion.servicio.actualizar_total()

        messages.success(request, f"Estado actualizado a {cotizacion.get_estado_cotizacion_display()}")
    else:
        messages.error(request, "Estado inválido")

    return redirect('cotizaciones:listar_cotizaciones')