from django.shortcuts import render,redirect
from django.contrib import messages

#modelos_cotizaciones 
from .models import Cotizacion
from .forms import CotizacionForm



def RegistrarCotizacion(request):
    
    if request.method == "POST":
        form = CotizacionForm(request.POST)

        if form.is_valid(): 
            form.save()
            messages.success(request, "Cotización registrada exitosamente.")    
            return redirect("listar_cotizaciones")
        else:
            messages.error(request, "Error al registrar la cotización.") 
    else:
        form = CotizacionForm()   
    return render(request, "cotizaciones/cotizacion_form.html", {"form": form})


    
def historial_cotizaciones(request):
    cotizaciones = Cotizacion.objects.all()

    cliente = request.GET.get('cliente')
    patente = request.GET.get('patente')

    if cliente:
        cotizaciones = cotizaciones.filter(cliente__nombre__icontains=cliente)
    if patente:
        cotizaciones = cotizaciones.filter(vehiculo__patente__icontains=patente)

    return render(request, 'cotizaciones/cotizacion_list.html', {
        'cotizaciones': cotizaciones
    })