"""Formularios de la aplicación Vehículos."""

from django import forms
from .models import Vehiculo, Servicio, Documento, normalizar_patente


class VehiculoForm(forms.ModelForm):
    """Formulario para crear y editar vehículos con validación de patente única."""
    
    class Meta:
        model = Vehiculo
        fields = ["patente", "marca", "modelo", "anio", "numero_chasis", "numero_motor", "cliente"]
        widgets = {
            "patente": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "AB1234 o ABCD12",
                    "pattern": "[A-Z]{2}[0-9]{4}|[A-Z]{4}[0-9]{2}",
                    "title": "Formato: AA1234 (antiguo) o ABCD12 (nuevo)",
                    "style": "text-transform: uppercase;",
                    "required": True 
                }
            ),
            "marca": forms.TextInput(attrs={"class": "form-control", "placeholder": "ej: Toyota"}),
            "modelo": forms.TextInput(attrs={"class": "form-control", "placeholder": "ej: Corolla"}),
            "anio": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1900",
                    "max": "2030",
                    "placeholder": "2024"
                }
            ),
            "numero_chasis": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "17 caracteres alfanuméricos",
                    "maxlength": "17"
                }
            ),
            "numero_motor": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": "20"
                }
            ),
            "cliente": forms.Select(
                attrs={
                    "class": "form-control",
                    "id": "id_cliente",
                    "required": True
                }
            ),
        }
    
    def clean_patente(self):
        """ 
        esta funcion se encarga de Valida que la patente no esté vacía y no esté duplicada 
        ."""
        patente = self.cleaned_data.get("patente")
        
        if not patente or not patente.strip():
            raise forms.ValidationError("La patente es obligatoria.")
        
        patente = normalizar_patente(patente)
        
        qs = Vehiculo.objects.exclude(pk=getattr(self.instance, "pk", None)).filter(
            patente__iexact=patente
        )
        if qs.exists():
            raise forms.ValidationError("Ya existe un vehículo con esa patente.")
        
        return patente
    
    def clean_cliente(self):
        """Valida que se haya seleccionado un cliente."""
        cliente = self.cleaned_data.get("cliente")
        
        if not cliente:
            raise forms.ValidationError("Debe seleccionar un cliente.")
        
        return cliente


class ServicioForm(forms.ModelForm):
    # Aceptar y mostrar fechas en formato chileno dd-mm-YYYY
    fecha_servicio = forms.DateField(
        input_formats=['%d-%m-%Y', '%d-%m-%y'],
        widget=forms.DateInput(format='%d-%m-%Y', attrs={
            'class': 'form-control',
            'placeholder': 'Seleccione una fecha',
            'readonly': 'readonly'
        })
    )
    
    vehiculo = forms.ModelChoiceField(
        queryset=Vehiculo.objects.all(),
        empty_label="Seleccione un vehículo",
        widget=forms.Select(attrs={'class': 'form-control',
                                   'placeholder': 'Seleccione un vehículo'}
    ))
    
    
    class Meta:
        model = Servicio
        fields = [
            'vehiculo',
            'fecha_servicio',
            'descripcion_trabajo',
            'diagnostico',
            'observaciones',
            'estado_servicio',
            'mano_obra',
            'repuestos'
        ]
        
        widgets = {
            'vehiculo': forms.Select(attrs={'class': 'form-control',
                                            'placeholder': 'Seleccione un vehículo'}),
            'fecha_servicio': forms.DateInput(format='%d-%m-%Y', attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione una fecha',
                'readonly': 'readonly'
            }),
            'descripcion_trabajo': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'diagnostico': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'estado_servicio': forms.Select(attrs={'class': 'form-control'}),
            'mano_obra': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'repuestos': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['tipo_documento', 'fecha_documento', 'monto', 'archivo']
        widgets = {
            'fecha_documento': forms.DateInput(
                attrs={
                    'type': 'date',  # genera el calendario
                    'class': 'form-control'
                }
            ),
            'tipo_documento': forms.Select(
                choices=[
                    ('Factura', 'Factura'),
                    ('Boleta', 'Boleta'),
                    ('Certificado', 'Certificado'),
                    ('Presupuesto', 'Presupuesto'),
                    ('Informe Técnico', 'Informe Técnico'),
                    ('Otro', 'Otro'),
                ],
                attrs={'class': 'form-control'}
            ),
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_archivo(self):
        archivo = self.cleaned_data.get('archivo', False)
        if archivo:
            ext = archivo.name.split('.')[-1].lower()
            if ext not in ['pdf', 'jpg', 'jpeg']:
                raise forms.ValidationError("Solo se permiten archivos PDF o JPG.")
        return archivo