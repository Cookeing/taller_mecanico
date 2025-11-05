from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Q
from django.contrib import messages

from .models import Vehiculo, Documento
from .forms import VehiculoForm, DocumentoForm
from clientes.models import Cliente
from clientes.forms import ClienteForm
from servicios.models import Servicio


def vehiculo_list(request):
    """
    Lista de vehículos con el cliente precargado.
    """
    vehiculos = (
        Vehiculo.objects
        .select_related("cliente")
        .all()
        .order_by("patente")
    )
    return render(request, "vehiculos/vehiculo_list.html", {"vehiculos": vehiculos})


def vehiculo_create(request):
    if request.method == "POST":
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
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
            return redirect("vehiculos:list")
    else:
        form = VehiculoForm(instance=vehiculo)

    # ojo: aquí solo mostramos el form de cliente si lo necesitas en el template
    return render(request, "vehiculos/vehiculo_form.html", {
        "form": form,
        "ClienteForm": ClienteForm(),
        "accion": "Editar",
    })


def vehiculo_delete(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == "POST":
        vehiculo.delete()
        return redirect("vehiculos:list")
    return render(request, "vehiculos/vehiculo_confirm_delete.html", {"vehiculo": vehiculo})


def vehiculo_detail(request, pk):
    """
    Muestra el vehículo + todos los servicios del vehículo + documentos de cada servicio.
    """
    vehiculo = get_object_or_404(
        Vehiculo.objects.select_related("cliente"),
        pk=pk,
    )

    # related_name='servicios' en Servicio -> vehiculo.servicios.all()
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


# ========== DOCUMENTOS DE UN SERVICIO ==========

def documentos_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    documentos = servicio.documentos.all().order_by('-fecha_documento')

    if request.method == "POST":
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.servicio = servicio
            doc.save()
            messages.success(request, "Documento subido con éxito.")
            return redirect("vehiculos:documentos_servicio", servicio_id=servicio.id)
    else:
        form = DocumentoForm()

    return render(request, "vehiculos/documentos_servicio.html", {
        "servicio": servicio,
        "documentos": documentos,
        "form": form,
    })


def documento_upload(request, servicio_id):
    servicio = get_object_or_404(Servicio, pk=servicio_id)
    if request.method == "POST":
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.servicio = servicio
            doc.save()
            messages.success(request, "Documento subido con éxito.")
    return redirect("vehiculos:documentos_servicio", servicio_id=servicio.id)


def documento_delete(request, pk):
    documento = get_object_or_404(Documento, pk=pk)
    servicio_id = documento.servicio.id
    if request.method == "POST":
        documento.delete()
        messages.success(request, "Documento eliminado correctamente.")
        return redirect("vehiculos:documentos_servicio", servicio_id=servicio_id)

    return render(request, "vehiculos/documento_confirm_delete.html", {
        "documento": documento,
    })


# ========== APIs PARA LOS JS DE BÚSQUEDA ==========

@require_GET
def buscar_vehiculos_api(request):
    """
    /vehiculos/api/buscar/?q=ABC
    Busca por patente.
    """
    q = request.GET.get("q", "").strip()
    if not q:
        return JsonResponse([], safe=False)

    vehiculos = (
        Vehiculo.objects
        .filter(patente__icontains=q)
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
    """
    /vehiculos/api/cliente/?q=juan
    Busca vehículos por nombre o RUT del cliente.
    """
    q = request.GET.get("q", "").strip()
    if not q:
        return JsonResponse([], safe=False)

    clientes = Cliente.objects.filter(
        Q(nombre__icontains=q) | Q(rut__icontains=q)
    )

    vehiculos = (
        Vehiculo.objects
        .filter(cliente__in=clientes)
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
