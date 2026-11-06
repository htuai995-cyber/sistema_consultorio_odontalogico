from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from gestion.models import Odontologo
from gestion.forms import OdontologoForm


@login_required
def odontologo_lista(request):
    q = request.GET.get('q', '')
    odontologos = Odontologo.objects.select_related('especialidad').all()
    if q:
        odontologos = odontologos.filter(
            Q(nombres__icontains=q) |
            Q(apellidos__icontains=q) |
            Q(numero_colegiatura__icontains=q) |
            Q(especialidad__nombre__icontains=q)
        )
    odontologos = odontologos.order_by('apellidos', 'nombres')
    paginator = Paginator(odontologos, 10)
    page = request.GET.get('page')
    odontologos_page = paginator.get_page(page)
    return render(request, 'gestion/odontologo/lista.html', {
        'odontologos': odontologos_page,
        'q': q,
        'total_registros': odontologos.count(),
        'titulo': 'Odontólogos',
    })


@login_required
def odontologo_crear(request):
    if request.method == 'POST':
        form = OdontologoForm(request.POST)
        if form.is_valid():
            od = form.save()
            messages.success(request, f'Odontólogo(a) {od.nombre_completo} registrado exitosamente.')
            return redirect('odontologo_lista')
    else:
        form = OdontologoForm()
    return render(request, 'gestion/odontologo/form.html', {
        'form': form,
        'titulo': 'Nuevo Odontólogo',
        'accion': 'Registrar',
    })


@login_required
def odontologo_editar(request, pk):
    odontologo = get_object_or_404(Odontologo, pk=pk)
    if request.method == 'POST':
        form = OdontologoForm(request.POST, instance=odontologo)
        if form.is_valid():
            form.save()
            messages.success(request, f'Odontólogo(a) {odontologo.nombre_completo} actualizado exitosamente.')
            return redirect('odontologo_lista')
    else:
        form = OdontologoForm(instance=odontologo)
    return render(request, 'gestion/odontologo/form.html', {
        'form': form,
        'titulo': f'Editar Odontólogo(a): {odontologo.nombre_completo}',
        'accion': 'Actualizar',
        'objeto': odontologo,
    })


@login_required
def odontologo_eliminar(request, pk):
    odontologo = get_object_or_404(Odontologo, pk=pk)
    if request.method == 'POST':
        try:
            nombre = odontologo.nombre_completo
            odontologo.delete()
            messages.success(request, f'Odontólogo(a) {nombre} eliminado exitosamente.')
        except Exception:
            messages.error(request, 'No se puede eliminar: tiene citas asociadas en el sistema.')
        return redirect('odontologo_lista')
    return render(request, 'gestion/confirmar_eliminar.html', {
        'objeto': odontologo,
        'titulo': 'Eliminar Odontólogo',
        'cancelar_url': 'odontologo_lista',
    })
