from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

from servicios.forms import DocumentoForm, FotoServicioForm
from .models import Documento, Servicio, FotoServicio
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


# ========== DOCUMENTOS DE UN SERVICIO ==========

def documentos_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    documentos = servicio.documentos.all().order_by('-fecha_documento')
    
    # AGREGADO: Cargar cotizaciones
    from cotizaciones.models import Cotizacion
    cotizaciones = Cotizacion.objects.filter(servicio=servicio).order_by('-fecha_emision')

    if request.method == "POST":
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.servicio = servicio
            doc.save()

            # ✅ ACTUALIZA TOTAL DEL SERVICIO
            servicio.actualizar_total()

            messages.success(request, "Documento subido con éxito.")
            return redirect("servicios:documentos_servicio", servicio_id=servicio.id)

    else:
        form = DocumentoForm()

    return render(request, "servicios/documentos_servicio.html", {
        "servicio": servicio,
        "documentos": documentos,
        "cotizaciones": cotizaciones,
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

            # 🚨 Agrega esto:
            servicio.actualizar_total()

            messages.success(request, "Documento subido con éxito.")
    return redirect("servicios:documentos_servicio", servicio_id=servicio.id)



def documento_delete(request, pk):
    documento = get_object_or_404(Documento, pk=pk)
    servicio = documento.servicio  # <<< usa esto en lugar de solo servicio_id
    if request.method == "POST":
        documento.delete()
        servicio.actualizar_total()  # <<< AÑADIR ESTA LÍNEA
        messages.success(request, "Documento eliminado correctamente.")
        return redirect("servicios:documentos_servicio", servicio_id=servicio.id)

    return render(request, "servicios/documento_confirm_delete.html", {
        "documento": documento,
    })



# ========== FOTOS DE SERVICIOS ==========

def optimizar_imagen(imagen, max_width=1920, max_height=1080, quality=85):
    """Optimiza una imagen redimensionándola y ajustando su calidad"""
    img = Image.open(imagen)
    
    # Convertir RGBA a RGB si es necesario (para PNGs con transparencia)
    if img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = background
    
    # Redimensionar manteniendo aspect ratio
    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
    
    # Guardar en buffer
    output = BytesIO()
    img.save(output, format='JPEG', quality=quality, optimize=True)
    output.seek(0)
    
    return output


def fotos_servicio(request, servicio_id):
    """Vista para subir y mostrar fotos de un servicio"""
    servicio = get_object_or_404(Servicio, id=servicio_id)
    fotos = servicio.fotos.all().order_by('-fecha_captura')
    
    if request.method == 'POST':
        form = FotoServicioForm(request.POST, request.FILES)
        if form.is_valid():
            imagenes = request.FILES.getlist('imagenes')
            descripcion = form.cleaned_data.get('descripcion', '')
            
            fotos_guardadas = 0
            for imagen in imagenes:
                try:
                    # Optimizar imagen
                    imagen_optimizada = optimizar_imagen(imagen)
                    
                    # Crear nombre de archivo
                    nombre_archivo = imagen.name
                    
                    # Crear objeto InMemoryUploadedFile
                    imagen_file = InMemoryUploadedFile(
                        imagen_optimizada,
                        'ImageField',
                        nombre_archivo,
                        'image/jpeg',
                        sys.getsizeof(imagen_optimizada),
                        None
                    )
                    
                    # Guardar foto
                    foto = FotoServicio(
                        servicio=servicio,
                        imagen=imagen_file,
                        descripcion=descripcion
                    )
                    foto.save()
                    fotos_guardadas += 1
                    
                except Exception as e:
                    messages.error(request, f"Error al procesar {imagen.name}: {str(e)}")
            
            if fotos_guardadas > 0:
                messages.success(request, f"✅ {fotos_guardadas} foto(s) subida(s) exitosamente.")
            
            return redirect('servicios:fotos_servicio', servicio_id=servicio.id)
    else:
        form = FotoServicioForm()
    
    return render(request, 'servicios/fotos_servicio.html', {
        'servicio': servicio,
        'fotos': fotos,
        'form': form
    })


def foto_delete(request, pk):
    """Elimina una foto de servicio"""
    foto = get_object_or_404(FotoServicio, pk=pk)
    servicio_id = foto.servicio.id
    
    if request.method == 'POST':
        foto.delete()
        messages.success(request, "🗑️ Foto eliminada correctamente.")
        return redirect('servicios:fotos_servicio', servicio_id=servicio_id)
    
    return render(request, 'servicios/foto_confirm_delete.html', {
        'foto': foto
    })