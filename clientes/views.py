"""
Vistas de la aplicación Clientes (CRUD) y endpoint de búsqueda (HU02).
Reemplaza completamente clientes/views.py con este contenido.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Cliente
from .forms import ClienteForm


def cliente_list(request):
    """
    Muestra la lista de clientes ordenados por nombre.
    Si se pasa el parámetro GET 'q', devuelve la lista filtrada (case-insensitive).
    Esta vista se usa como la página principal de clientes y soporta búsqueda server-side.

    """
    q = request.GET.get('q', '').strip()
    if q:
        clientes = Cliente.objects.filter(nombre__icontains=q).order_by('nombre')
    else:
        clientes = Cliente.objects.all().order_by('nombre')
    return render(request, 'clientes/cliente_list.html', {'clientes': clientes, 'query': q})


def cliente_create(request):
    """Crea un nuevo cliente."""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes:list')
    else:
        form = ClienteForm()
    return render(request, 'clientes/cliente_form.html', {'form': form, 'accion': 'Crear'})


def cliente_update(request, pk: int):
    """Edita un cliente existente."""
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes:list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/cliente_form.html', {'form': form, 'accion': 'Editar'})


def cliente_delete(request, pk: int):
    """Elimina un cliente con confirmación previa."""
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('clientes:list')
    return render(request, 'clientes/cliente_confirm_delete.html', {'cliente': cliente})


@require_GET
def buscar_clientes_api(request):
    """
    Endpoint JSON para búsqueda dinámica (live search).
    Recibe GET 'q' y devuelve una lista JSON con campos id, nombre, rut, telefono.
    Ejemplo: GET /clientes/api/buscar/?q=juan
    """
    q = request.GET.get('q', '').strip()
    
    if not q:
        # Retornar lista vacía para evitar exponer todo el catálogo en cada pulsación
        return JsonResponse([], safe=False)
    qs = Cliente.objects.filter(nombre__icontains=q).order_by('nombre')[:50]
    data = list(qs.values('id', 'nombre', 'rut', 'telefono'))
    return JsonResponse(data, safe=False)
