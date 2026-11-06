from django import forms
from gestion.models import Tratamiento, Diagnostico


class TratamientoForm(forms.ModelForm):
    class Meta:
        model = Tratamiento
        fields = ['diagnostico', 'nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'costo', 'estado']
        widgets = {
            'diagnostico': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del tratamiento'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción del procedimiento'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'costo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'placeholder': '0.00'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['diagnostico'].queryset = Diagnostico.objects.select_related('cita__paciente').all()
        self.fields['diagnostico'].label_from_instance = lambda obj: f"Diag. #{obj.id} - {obj.cita.paciente.nombre_completo} ({obj.fecha})"

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            raise forms.ValidationError('La fecha de fin no puede ser anterior a la fecha de inicio.')
        return cleaned_data
