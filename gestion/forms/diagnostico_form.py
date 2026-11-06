from django import forms
from gestion.models import Diagnostico, Cita


class DiagnosticoForm(forms.ModelForm):
    class Meta:
        model = Diagnostico
        fields = ['cita', 'descripcion', 'recomendaciones', 'fecha']
        widgets = {
            'cita': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Diagnóstico clínico detallado'}),
            'recomendaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Recomendaciones para el paciente'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cita'].queryset = Cita.objects.select_related('paciente', 'odontologo').all()
        self.fields['cita'].label_from_instance = lambda obj: f"Cita #{obj.id} - {obj.paciente.nombre_completo} ({obj.fecha} {obj.hora.strftime('%H:%M')})"
