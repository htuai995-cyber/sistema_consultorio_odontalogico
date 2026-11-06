from django.contrib import admin
from gestion.models import Especialidad, Paciente, Odontologo, Cita, Diagnostico, Tratamiento, Receta


@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'estado']
    list_filter = ['estado']
    search_fields = ['nombre']


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['id', 'apellidos', 'nombres', 'dni', 'telefono', 'created_at']
    search_fields = ['nombres', 'apellidos', 'dni']


@admin.register(Odontologo)
class OdontologoAdmin(admin.ModelAdmin):
    list_display = ['id', 'apellidos', 'nombres', 'numero_colegiatura', 'especialidad', 'estado']
    list_filter = ['estado', 'especialidad']
    search_fields = ['nombres', 'apellidos', 'numero_colegiatura']


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ['id', 'paciente', 'odontologo', 'fecha', 'hora', 'estado']
    list_filter = ['estado', 'fecha']
    search_fields = ['paciente__nombres', 'paciente__apellidos']


@admin.register(Diagnostico)
class DiagnosticoAdmin(admin.ModelAdmin):
    list_display = ['id', 'cita', 'fecha']
    search_fields = ['cita__paciente__nombres']


@admin.register(Tratamiento)
class TratamientoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'diagnostico', 'fecha_inicio', 'fecha_fin', 'costo', 'estado']
    list_filter = ['estado']
    search_fields = ['nombre']


@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = ['id', 'medicamento', 'diagnostico', 'dosis', 'fecha_emision']
    search_fields = ['medicamento']
