from django import forms
from gestion.models import Cita, Paciente, Odontologo


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['paciente', 'odontologo', 'fecha', 'hora', 'motivo', 'estado', 'observaciones']
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'odontologo': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'motivo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Motivo de consulta'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observaciones adicionales'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['odontologo'].queryset = Odontologo.objects.filter(estado='Activo')
        self.fields['paciente'].label_from_instance = lambda obj: f"{obj.apellidos}, {obj.nombres} (DNI: {obj.dni})"
        self.fields['odontologo'].label_from_instance = lambda obj: f"Dr(a). {obj.apellidos}, {obj.nombres} - {obj.especialidad.nombre}"
