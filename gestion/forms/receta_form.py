from django import forms
from gestion.models import Receta, Diagnostico


class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['diagnostico', 'medicamento', 'dosis', 'frecuencia', 'duracion', 'indicaciones', 'fecha_emision']
        widgets = {
            'diagnostico': forms.Select(attrs={'class': 'form-select'}),
            'medicamento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del medicamento'}),
            'dosis': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 500mg'}),
            'frecuencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Cada 8 horas'}),
            'duracion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 7 días'}),
            'indicaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Indicaciones adicionales'}),
            'fecha_emision': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['diagnostico'].queryset = Diagnostico.objects.select_related('cita__paciente').all()
        self.fields['diagnostico'].label_from_instance = lambda obj: f"Diag. #{obj.id} - {obj.cita.paciente.nombre_completo} ({obj.fecha})"
