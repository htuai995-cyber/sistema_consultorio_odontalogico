from django import forms
from gestion.models import Especialidad


class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ['nombre', 'descripcion', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la especialidad'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'estado': 'Estado',
        }

