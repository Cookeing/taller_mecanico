from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib import messages
from django.utils import timezone
from .models import Cliente
from .forms import ClienteForm


def cliente_list(request):
    """Muestra solo clientes activos"""
    q = request.GET.get('q', '').strip()
    if q:
        clientes = Cliente.objects.filter(activo=True, nombre__icontains=q).order_by('nombre')
    else:
        clientes = Cliente.objects.filter(activo=True).order_by('nombre')
    return render(request, 'clientes/cliente_list.html', {'clientes': clientes, 'query': q})


def cliente_create(request):
    """Crea un nuevo cliente."""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            # Si se creó desde un popup devolver plantilla ligera que cierre la ventana
            if request.GET.get('popup') == '1':
                return render(request, 'vehiculos/popup_cliente.html', {'cliente': cliente})

            messages.success(request, '✅ Cliente creado exitosamente.')
            return redirect('clientes:list')
    else:
        form = ClienteForm()
    # pasar flag popup al template si se abrió como popup
    is_popup = request.GET.get('popup') == '1'
    return render(request, 'clientes/cliente_form.html', {'form': form, 'accion': 'Crear', 'popup': is_popup})


def cliente_update(request, pk: int):
    """Edita un cliente existente."""
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Cliente actualizado exitosamente.')
            return redirect('clientes:list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/cliente_form.html', {'form': form, 'accion': 'Editar'})


def cliente_delete(request, pk: int):
    """Desactiva un cliente (soft delete)"""
    cliente = get_object_or_404(Cliente, pk=pk)
    
    # Contar vehículos activos
    vehiculos_activos = cliente.vehiculos.filter(activo=True)
    
    if request.method == 'POST':
        cliente.activo = False
        cliente.fecha_eliminacion = timezone.now()
        cliente.save()
        messages.success(request, f'✅ Cliente {cliente.nombre} desactivado exitosamente.')
        return redirect('clientes:list')
    
    return render(request, 'clientes/cliente_confirm_delete.html', {
        'cliente': cliente,
        'vehiculos_activos': vehiculos_activos
    })


@require_GET
def buscar_clientes_api(request):
    """API para búsqueda - solo clientes activos"""
    q = request.GET.get('q', '').strip()
    if not q:
        return JsonResponse([], safe=False)
    qs = Cliente.objects.filter(activo=True, nombre__icontains=q).order_by('nombre')[:50]
    data = list(qs.values('id', 'nombre', 'rut', 'telefono'))
    return JsonResponse(data, safe=False)


def clientes_inactivos(request):
    """Vista para gestionar clientes inactivos"""
    clientes = Cliente.objects.filter(activo=False).order_by('-fecha_eliminacion')
    return render(request, 'clientes/clientes_inactivos.html', {'clientes': clientes})


def cliente_reactivar(request, pk: int):
    """Reactiva un cliente inactivo"""
    cliente = get_object_or_404(Cliente, pk=pk, activo=False)
    if request.method == 'POST':
        cliente.activo = True
        cliente.fecha_eliminacion = None
        cliente.save()
        messages.success(request, f'✅ Cliente {cliente.nombre} reactivado exitosamente.')
        return redirect('clientes:inactivos')
    return render(request, 'clientes/cliente_confirm_reactivar.html', {'cliente': cliente})
