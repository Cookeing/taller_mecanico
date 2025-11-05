from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Servicio
from .forms import ServicioForm


def servicio_list(request):
    """Lista todos los servicios registrados, ordenados por fecha."""
    servicios = (
        Servicio.objects
        .select_related('vehiculo', 'vehiculo__cliente')
        .order_by('-fecha_servicio')
    )
    return render(request, 'servicios/servicio_list.html', {'servicios': servicios})


def servicio_create(request):
    """Crea un nuevo servicio asociado a un vehículo."""
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            servicio = form.save(commit=False)

            # Asigna el total manual ingresado en el formulario
            total_ingresado = form.cleaned_data.get('total', 0)
            servicio.total = total_ingresado
            servicio.save()

            # Actualiza el total solo si hay documentos asociados
            servicio.actualizar_total()

            messages.success(request, '✅ Servicio registrado correctamente.')
            return redirect('servicios:list')
        else:
            messages.error(request, '❌ Corrige los errores del formulario antes de continuar.')
    else:
        form = ServicioForm()

    return render(request, 'servicios/servicio_form.html', {
        'form': form,
        'accion': 'Registrar'
    })


def servicio_update(request, pk):
    """Edita un servicio existente."""
    servicio = get_object_or_404(Servicio, pk=pk)

    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            # Guardamos el formulario sin commit
            servicio_modificado = form.save(commit=False)

            # Asignamos el total desde el formulario (si cambió)
            nuevo_total = form.cleaned_data.get('total')
            if nuevo_total is not None:
                # Convertimos a Decimal correctamente
                from decimal import Decimal
                try:
                    nuevo_total = Decimal(nuevo_total)
                except:
                    nuevo_total = Decimal('0.00')
                servicio_modificado.total = nuevo_total

            # Guardamos el registro actualizado en la base de datos
            servicio_modificado.save(force_update=True)

            # Recalcula solo si hay documentos asociados (para no borrar el total manual)
            documentos = servicio_modificado.documentos.all()
            if documentos.exists():
                servicio_modificado.actualizar_total()

            messages.success(request, '✅ Servicio actualizado correctamente.')
            return redirect('servicios:list')
        else:
            messages.error(request, '❌ Corrige los errores antes de continuar.')
    else:
        form = ServicioForm(instance=servicio)

    return render(request, 'servicios/servicio_form.html', {
        'form': form,
        'accion': 'Editar',
    })




def servicio_delete(request, pk):
    """Elimina un servicio con confirmación."""
    servicio = get_object_or_404(Servicio, pk=pk)

    if request.method == 'POST':
        servicio.delete()
        messages.success(request, '🗑️ Servicio eliminado correctamente.')
        return redirect('servicios:list')

    return render(request, 'servicios/servicio_confirm_delete.html', {
        'servicio': servicio
    })

from django.views.decorators.http import require_POST

@require_POST
def cambiar_estado_servicio(request, pk):
    """Permite cambiar el estado de un servicio desde la tabla."""
    servicio = get_object_or_404(Servicio, pk=pk)
    nuevo_estado = request.POST.get('estado')

    estados_validos = [e[0] for e in Servicio.ESTADOS]
    if nuevo_estado not in estados_validos:
        messages.error(request, "❌ Estado no válido.")
    else:
        servicio.estado = nuevo_estado
        servicio.save(update_fields=['estado'])
        messages.success(request, f"✅ Estado actualizado a: {servicio.get_estado_display()}.")

    return redirect('servicios:list')
