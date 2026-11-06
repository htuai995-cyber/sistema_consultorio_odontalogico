from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from gestion.models import Especialidad
from gestion.forms import EspecialidadForm


@login_required
def especialidad_lista(request):
    q = request.GET.get('q', '')
    especialidades = Especialidad.objects.all()
    if q:
        especialidades = especialidades.filter(
            Q(nombre__icontains=q) | Q(descripcion__icontains=q)
        )
    especialidades = especialidades.order_by('nombre')
    paginator = Paginator(especialidades, 10)
    page = request.GET.get('page')
    especialidades_page = paginator.get_page(page)
    return render(request, 'gestion/especialidad/lista.html', {
        'especialidades': especialidades_page,
        'q': q,
        'total_registros': especialidades.count(),
        'titulo': 'Especialidades',
    })


@login_required
def especialidad_crear(request):
    if request.method == 'POST':
        form = EspecialidadForm(request.POST)
        if form.is_valid():
            esp = form.save()
            messages.success(request, f'Especialidad "{esp.nombre}" registrada exitosamente.')
            return redirect('especialidad_lista')
    else:
        form = EspecialidadForm()
    return render(request, 'gestion/especialidad/form.html', {
        'form': form,
        'titulo': 'Nueva Especialidad',
        'accion': 'Registrar',
    })


@login_required
def especialidad_editar(request, pk):
    especialidad = get_object_or_404(Especialidad, pk=pk)
    if request.method == 'POST':
        form = EspecialidadForm(request.POST, instance=especialidad)
        if form.is_valid():
            form.save()
            messages.success(request, f'Especialidad "{especialidad.nombre}" actualizada exitosamente.')
            return redirect('especialidad_lista')
    else:
        form = EspecialidadForm(instance=especialidad)
    return render(request, 'gestion/especialidad/form.html', {
        'form': form,
        'titulo': f'Editar Especialidad: {especialidad.nombre}',
        'accion': 'Actualizar',
        'objeto': especialidad,
    })


@login_required
def especialidad_eliminar(request, pk):
    especialidad = get_object_or_404(Especialidad, pk=pk)
    if request.method == 'POST':
        try:
            nombre = especialidad.nombre
            especialidad.delete()
            messages.success(request, f'Especialidad "{nombre}" eliminada exitosamente.')
        except Exception:
            messages.error(request, 'No se puede eliminar la especialidad: tiene odontólogos asociados.')
        return redirect('especialidad_lista')
    return render(request, 'gestion/confirmar_eliminar.html', {
        'objeto': especialidad,
        'titulo': 'Eliminar Especialidad',
        'cancelar_url': 'especialidad_lista',
    })
