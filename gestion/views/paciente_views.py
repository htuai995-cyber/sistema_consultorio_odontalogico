from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from gestion.models import Paciente
from gestion.forms import PacienteForm


@login_required
def paciente_lista(request):
    q = request.GET.get('q', '')
    pacientes = Paciente.objects.all()
    if q:
        pacientes = pacientes.filter(
            Q(nombres__icontains=q) |
            Q(apellidos__icontains=q) |
            Q(dni__icontains=q) |
            Q(telefono__icontains=q)
        )
    pacientes = pacientes.order_by('apellidos', 'nombres')
    paginator = Paginator(pacientes, 10)
    page = request.GET.get('page')
    pacientes_page = paginator.get_page(page)
    return render(request, 'gestion/paciente/lista.html', {
        'pacientes': pacientes_page,
        'q': q,
        'total_registros': pacientes.count(),
        'titulo': 'Pacientes',
    })


@login_required
def paciente_detalle(request, pk):
    from gestion.models import Diagnostico, Tratamiento, Receta
    paciente = get_object_or_404(Paciente, pk=pk)
    citas = paciente.citas.all().select_related('odontologo').order_by('-fecha', '-hora')
    diagnosticos = Diagnostico.objects.filter(cita__paciente=paciente).select_related('cita__odontologo').order_by('-fecha')
    tratamientos = Tratamiento.objects.filter(diagnostico__cita__paciente=paciente).select_related('diagnostico').order_by('-fecha_inicio')
    recetas = Receta.objects.filter(diagnostico__cita__paciente=paciente).select_related('diagnostico').order_by('-fecha_emision')

    return render(request, 'gestion/paciente/detalle.html', {
        'paciente': paciente,
        'citas': citas,
        'diagnosticos': diagnosticos,
        'tratamientos': tratamientos,
        'recetas': recetas,
        'titulo': f'Historial Clínico: {paciente.nombre_completo}',
    })


@login_required
def paciente_crear(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            pac = form.save()
            messages.success(request, f'Paciente {pac.nombre_completo} registrado exitosamente.')
            return redirect('paciente_lista')
    else:
        form = PacienteForm()
    return render(request, 'gestion/paciente/form.html', {
        'form': form,
        'titulo': 'Nuevo Paciente',
        'accion': 'Registrar',
    })


@login_required
def paciente_editar(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, f'Paciente {paciente.nombre_completo} actualizado exitosamente.')
            return redirect('paciente_lista')
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'gestion/paciente/form.html', {
        'form': form,
        'titulo': f'Editar Paciente: {paciente.nombre_completo}',
        'accion': 'Actualizar',
        'objeto': paciente,
    })


@login_required
def paciente_eliminar(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == 'POST':
        try:
            nombre = paciente.nombre_completo
            paciente.delete()
            messages.success(request, f'Paciente {nombre} eliminado exitosamente.')
        except Exception:
            messages.error(request, 'No se puede eliminar el paciente porque tiene citas u otros registros vinculados.')
        return redirect('paciente_lista')
    return render(request, 'gestion/confirmar_eliminar.html', {
        'objeto': paciente,
        'titulo': 'Eliminar Paciente',
        'cancelar_url': 'paciente_lista',
    })
