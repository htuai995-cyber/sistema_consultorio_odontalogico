from django import forms
from gestion.models import Odontologo, Especialidad


class OdontologoForm(forms.ModelForm):
    class Meta:
        model = Odontologo
        fields = ['nombres', 'apellidos', 'numero_colegiatura', 'telefono', 'correo', 'especialidad', 'estado']
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'numero_colegiatura': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'N° Colegiatura'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'especialidad': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['especialidad'].queryset = Especialidad.objects.filter(estado='Activa')

