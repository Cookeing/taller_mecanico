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
        # Solo cliente y patente son obligatorios
        self.fields['cliente'].required = True
        self.fields['patente'].required = True
        self.fields['marca'].required = False
        self.fields['modelo'].required = False
        self.fields['anio'].required = False
        self.fields['chasis'].required = False
        self.fields['motor'].required = False
        self.fields['kilometraje'].required = False
        
        # Filtrar solo clientes activos
        from clientes.models import Cliente
        self.fields['cliente'].queryset = Cliente.objects.filter(activo=True).order_by('nombre')
