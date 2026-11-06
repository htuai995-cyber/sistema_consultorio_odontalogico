from django import forms
from gestion.models import Paciente


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombres', 'apellidos', 'dni', 'fecha_nacimiento', 'telefono', 'direccion', 'correo']
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'dni': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00000000', 'maxlength': '8'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección completa'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
        }

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if not dni.isdigit():
            raise forms.ValidationError('El DNI debe contener solo dígitos.')
        if len(dni) != 8:
            raise forms.ValidationError('El DNI debe tener exactamente 8 dígitos.')
        return dni

