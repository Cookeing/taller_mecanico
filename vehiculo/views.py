from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone

from .models import Vehiculo 
from .forms import VehiculoForm
from clientes.models import Cliente
from clientes.forms import ClienteForm


def vehiculo_list(request):
    """Lista solo vehículos activos de clientes activos"""
    vehiculos = (
        Vehiculo.objects
        .filter(activo=True, cliente__activo=True)
        .select_related("cliente")
        .order_by("patente")
    )
    return render(request, "vehiculos/vehiculo_list.html", {"vehiculos": vehiculos})


def vehiculo_create(request):
    if request.method == "POST":
        form = VehiculoForm(request.POST)
        if form.is_valid():
            vehiculo = form.save()

            # Si viene en modo popup va a devolver template especial osea el que se creo xd
            if request.GET.get("popup") == "1":
                return render(request, "servicios/popup_vehiculo.html", {"vehiculo": vehiculo})

            messages.success(request, "Vehículo registrado exitosamente.")
            return redirect("vehiculos:list")
    else:
        form = VehiculoForm()

    return render(request, "vehiculos/vehiculo_form.html", {
        "form": form,
        "accion": "Registrar",
    })



def vehiculo_update(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == "POST":
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Vehículo actualizado exitosamente.')
            return redirect("vehiculos:list")
    else:
        form = VehiculoForm(instance=vehiculo)
    return render(request, "vehiculos/vehiculo_form.html", {
        "form": form,
        "ClienteForm": ClienteForm(),
        "accion": "Editar",
    })


def vehiculo_delete(request, pk):
    """Desactiva un vehículo (soft delete)"""
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    
    # Contar servicios asociados
    servicios_count = vehiculo.servicios.count()
    
    if request.method == "POST":
        vehiculo.activo = False
        vehiculo.fecha_eliminacion = timezone.now()
        vehiculo.save()
        messages.success(request, f'✅ Vehículo {vehiculo.patente} desactivado exitosamente.')
        return redirect("vehiculos:list")
    
    return render(request, "vehiculos/vehiculo_confirm_delete.html", {
        "vehiculo": vehiculo,
        "servicios_count": servicios_count,
    })


def vehiculo_detail(request, pk):
    """Muestra el vehículo + servicios"""
    vehiculo = get_object_or_404(
        Vehiculo.objects.select_related("cliente"),
        pk=pk,
    )
    servicios = (
        vehiculo.servicios
        .all()
        .prefetch_related("documentos")
        .order_by("-fecha_servicio")
    )
    return render(request, "vehiculos/vehiculo_detail.html", {
        "vehiculo": vehiculo,
        "servicios": servicios,
    })


@require_GET
def buscar_vehiculos_api(request):
    """API búsqueda por patente - solo vehículos activos"""
    q = request.GET.get("q", "").strip()
    if not q:
        return JsonResponse([], safe=False)
    vehiculos = (
        Vehiculo.objects
        .filter(activo=True, cliente__activo=True, patente__icontains=q)
        .select_related("cliente")[:50]
    )
    data = []
    for v in vehiculos:
        data.append({
            "id": v.id,
            "patente": v.patente,
            "marca": v.marca or "",
            "modelo": v.modelo or "",
            "cliente": v.cliente.nombre if v.cliente else "",
            "cliente_rut": v.cliente.rut if v.cliente else "",
        })
    return JsonResponse(data, safe=False)


@require_GET
def buscar_vehiculos_por_cliente_api(request):
    """API búsqueda por cliente - solo activos"""
    q = request.GET.get("q", "").strip()
    if not q:
        return JsonResponse([], safe=False)
    
    # CORRECCIÓN: Primero hacer el filtro con Q, LUEGO agregar activo=True
    clientes = Cliente.objects.filter(
        Q(nombre__icontains=q) | Q(rut__icontains=q)
    ).filter(activo=True)
    
    vehiculos = (
        Vehiculo.objects
        .filter(activo=True, cliente__in=clientes)
        .select_related("cliente")[:50]
    )
    data = []
    for v in vehiculos:
        data.append({
            "id": v.id,
            "patente": v.patente,
            "marca": v.marca or "",
            "modelo": v.modelo or "",
            "cliente": v.cliente.nombre if v.cliente else "",
            "cliente_rut": v.cliente.rut if v.cliente else "",
        })
    return JsonResponse(data, safe=False)



def vehiculos_inactivos(request):
    """Vista para gestionar vehículos inactivos"""
    vehiculos = Vehiculo.objects.filter(activo=False).select_related('cliente').order_by('-fecha_eliminacion')
    return render(request, 'vehiculos/vehiculos_inactivos.html', {'vehiculos': vehiculos})


def vehiculo_reactivar(request, pk: int):
    """Reactiva un vehículo inactivo"""
    vehiculo = get_object_or_404(Vehiculo, pk=pk, activo=False)
    if request.method == 'POST':
        vehiculo.activo = True
        vehiculo.fecha_eliminacion = None
        vehiculo.save()
        messages.success(request, f'✅ Vehículo {vehiculo.patente} reactivado exitosamente.')
        return redirect('vehiculos:inactivos')
    return render(request, 'vehiculos/vehiculo_confirm_reactivar.html', {'vehiculo': vehiculo})
