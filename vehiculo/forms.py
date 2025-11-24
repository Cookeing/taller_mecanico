from django import forms
from .models import Vehiculo




class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['cliente', 'patente', 'marca', 'modelo', 'anio', 'chasis', 'motor', 'kilometraje']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'patente': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'anio': forms.NumberInput(attrs={'class': 'form-control'}),
            'chasis': forms.TextInput(attrs={'class': 'form-control'}),
            'motor': forms.TextInput(attrs={'class': 'form-control'}),
            'kilometraje': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer todos los campos obligatorios
        self.fields['cliente'].required = True
        self.fields['patente'].required = True
        self.fields['marca'].required = True
        self.fields['modelo'].required = True
        self.fields['anio'].required = True
        self.fields['chasis'].required = True
        self.fields['motor'].required = True
        self.fields['kilometraje'].required = True
        
        # Filtrar solo clientes activos
        from clientes.models import Cliente
        self.fields['cliente'].queryset = Cliente.objects.filter(activo=True).order_by('nombre')
