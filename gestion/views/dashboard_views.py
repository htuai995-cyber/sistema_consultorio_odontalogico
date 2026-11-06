from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from gestion.models import Paciente, Odontologo, Cita, Diagnostico, Tratamiento, Receta, Especialidad
from django.utils import timezone


@login_required
def dashboard(request):
    hoy = timezone.now().date()
    total_pacientes = Paciente.objects.count()
    total_odontologos = Odontologo.objects.filter(estado='Activo').count()
    total_citas = Cita.objects.count()
    citas_hoy = Cita.objects.filter(fecha=hoy).count()
    citas_pendientes = Cita.objects.filter(estado='Pendiente').count()
    citas_confirmadas = Cita.objects.filter(estado='Confirmada').count()
    total_diagnosticos = Diagnostico.objects.count()
    total_tratamientos = Tratamiento.objects.count()
    tratamientos_en_proceso = Tratamiento.objects.filter(estado='En proceso').count()
    total_recetas = Receta.objects.count()
    total_especialidades = Especialidad.objects.filter(estado='Activa').count()

    # Últimas citas
    ultimas_citas = Cita.objects.select_related('paciente', 'odontologo').order_by('-fecha', '-hora')[:5]

    # Últimos pacientes
    ultimos_pacientes = Paciente.objects.order_by('-created_at')[:5]

    return render(request, 'gestion/dashboard.html', {
        'titulo': 'Dashboard',
        'total_pacientes': total_pacientes,
        'total_odontologos': total_odontologos,
        'total_citas': total_citas,
        'citas_hoy': citas_hoy,
        'citas_pendientes': citas_pendientes,
        'citas_confirmadas': citas_confirmadas,
        'total_diagnosticos': total_diagnosticos,
        'total_tratamientos': total_tratamientos,
        'tratamientos_en_proceso': tratamientos_en_proceso,
        'total_recetas': total_recetas,
        'total_especialidades': total_especialidades,
        'ultimas_citas': ultimas_citas,
        'ultimos_pacientes': ultimos_pacientes,
        'hoy': hoy,
    })

