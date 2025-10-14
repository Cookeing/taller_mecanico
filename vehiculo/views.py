from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db import models
from .models import Vehiculo
from clientes.models import Cliente
from .forms import VehiculoForm
# modulo especifico de el formulario de clientes
from clientes.forms import ClienteForm

def vehiculo_list(request):
    """Página HTML con tabla y dos barras de búsqueda (clientes/vehículos)."""
    # mostramos todos por defecto (la búsqueda dinámica se hace vía JS -> API)
    vehiculos = Vehiculo.objects.select_related("cliente").all().order_by("patente")
    return render(request, "vehiculos/vehiculo_list.html", {"vehiculos": vehiculos})


def vehiculo_create(request):
    """Crea un nuevo vehículo."""
    if request.method == "POST":
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("vehiculos:list")
    else:
        form = VehiculoForm()
    
    return render(request, "vehiculos/vehiculo_form.html", {
        "form": form,
        "accion": "Registrar"
    })
    

def vehiculo_update(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == "POST":
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            return redirect("vehiculos:list")
    else:
        form = VehiculoForm(instance=vehiculo)
    return render(request, "vehiculos/vehiculo_form.html", {"form": form,
                                                            "ClienteForm": ClienteForm(), #aqui esta el formulario de cliente
                                                            "accion": "Editar"})    


def vehiculo_delete(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == "POST":
        vehiculo.delete()
        return redirect("vehiculos:list")
    return render(request, "vehiculos/vehiculo_confirm_delete.html", {"vehiculo": vehiculo})


def vehiculo_detail(request, pk):
    # 1. Obtenemos el vehículo y precargamos el cliente para evitar consultas extras.
    vehiculo = get_object_or_404(Vehiculo.objects.select_related("cliente"), pk=pk)

    # 2. Obtenemos todos los servicios asociados al vehículo.
    #    Hacemos un 'prefetch_related' para obtener los documentos de TODOS los servicios
    #    en una sola consulta eficiente, en lugar de una consulta por cada servicio.
    servicios = vehiculo.servicios.all().order_by("-fecha_servicio").prefetch_related("documentos")
    
    # NOTA: Ahora, cada objeto 's' en 'servicios' ya tiene cargado su s.documento_set.all()
    #       (gracias a prefetch_related), lo que hace que la plantilla sea simple.

    # 3. Preparamos el contexto. Ya no necesitamos 'documentos_por_servicio'.
    context = {
        "vehiculo": vehiculo,
        "servicios": servicios,
        # "documentos_por_servicio" ya no es necesario
    }
    
    return render(request, "vehiculos/vehiculo_detail.html", context)


@require_GET
def buscar_vehiculos_api(request):
    """
    Endpoint JSON para live-search de vehículos por patente.
    Ej: /vehiculos/api/buscar/?q=ABC
    """
    q = request.GET.get("q", "").strip()
    if not q:
        return JsonResponse([], safe=False)

    # Búsqueda más eficiente con icontains
    qs = Vehiculo.objects.filter(patente__icontains=q).select_related("cliente")[:50]
    data = []
    for v in qs:
        data.append({
            "id": v.id,
            "patente": v.patente,
            "marca": v.marca or "",
            "modelo": v.modelo or "",
            "cliente": v.cliente.nombre if v.cliente else "",
            "cliente_rut": v.cliente.rut if v.cliente else "",
        })
    return JsonResponse(data, safe=False)

def buscar_vehiculos_por_cliente_api(request):
    """
    Endpoint JSON para buscar vehículos por cliente (nombre o RUT).
    Ej: /vehiculos/api/buscar-por-cliente/?q=juan
    """
    q = request.GET.get("q", "").strip()
    if not q:
        return JsonResponse([], safe=False)

    try:
        # Buscar clientes que coincidan con la query
        clientes_coincidentes = Cliente.objects.filter(
            models.Q(nombre__icontains=q) | models.Q(rut__icontains=q)
        )
        
        # Obtener vehículos de esos clientes
        vehiculos = Vehiculo.objects.filter(
            cliente__in=clientes_coincidentes
        ).select_related("cliente")[:50]
        
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
    
    except Exception as e:
        # Para debugging - muestra el error en la consola
        print(f"Error en búsqueda por cliente: {e}")
        return JsonResponse([], safe=False)