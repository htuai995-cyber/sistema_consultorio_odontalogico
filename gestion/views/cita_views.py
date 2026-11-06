from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.utils import timezone
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import io
from gestion.models import Cita
from gestion.forms import CitaForm


@login_required
def cita_lista(request):
    q = request.GET.get('q', '')
    estado = request.GET.get('estado', '')
    fecha = request.GET.get('fecha', '')
    citas = Cita.objects.select_related('paciente', 'odontologo').all()

    if q:
        citas = citas.filter(
            paciente__nombres__icontains=q) | Cita.objects.filter(
            paciente__apellidos__icontains=q) | Cita.objects.filter(
            odontologo__apellidos__icontains=q)
    if estado:
        citas = citas.filter(estado=estado)
    if fecha:
        citas = citas.filter(fecha=fecha)

    citas = citas.distinct().order_by('-fecha', '-hora')
    paginator = Paginator(citas, 10)
    page = request.GET.get('page')
    citas_page = paginator.get_page(page)

    return render(request, 'gestion/cita/lista.html', {
        'citas': citas_page,
        'q': q,
        'estado': estado,
        'fecha': fecha,
        'total_registros': citas.count(),
        'titulo': 'Citas',
        'estados': ['Pendiente', 'Confirmada', 'Atendida', 'Cancelada'],
    })


@login_required
def cita_crear(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save()
            messages.success(request, f'Cita #{cita.id} registrada exitosamente.')
            return redirect('cita_lista')
    else:
        form = CitaForm()
    return render(request, 'gestion/cita/form.html', {
        'form': form,
        'titulo': 'Nueva Cita',
        'accion': 'Registrar',
    })


@login_required
def cita_editar(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.success(request, f'Cita #{cita.id} actualizada exitosamente.')
            return redirect('cita_lista')
    else:
        form = CitaForm(instance=cita)
    return render(request, 'gestion/cita/form.html', {
        'form': form,
        'titulo': f'Editar Cita #{cita.id}',
        'accion': 'Actualizar',
        'objeto': cita,
    })


@login_required
def cita_eliminar(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    if request.method == 'POST':
        try:
            cita.delete()
            messages.success(request, f'Cita #{pk} eliminada exitosamente.')
        except Exception:
            messages.error(request, 'No se puede eliminar: tiene diagnósticos asociados.')
        return redirect('cita_lista')
    return render(request, 'gestion/confirmar_eliminar.html', {
        'objeto': cita,
        'titulo': 'Eliminar Cita',
        'cancelar_url': 'cita_lista',
    })


@login_required
def cita_reporte_pdf(request):
    q = request.GET.get('q', '')
    estado = request.GET.get('estado', '')
    fecha = request.GET.get('fecha', '')

    citas = Cita.objects.select_related('paciente', 'odontologo').all()
    filtros = []

    if q:
        citas = citas.filter(
            paciente__nombres__icontains=q) | Cita.objects.filter(
            paciente__apellidos__icontains=q) | Cita.objects.filter(
            odontologo__apellidos__icontains=q)
        filtros.append(f'Búsqueda: "{q}"')
    if estado:
        citas = citas.filter(estado=estado)
        filtros.append(f'Estado: {estado}')
    if fecha:
        citas = citas.filter(fecha=fecha)
        filtros.append(f'Fecha: {fecha}')

    citas = citas.distinct().order_by('-fecha', '-hora')

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        leftMargin=1.5*cm,
        rightMargin=1.5*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm
    )
    styles = getSampleStyleSheet()
    elements = []

    # Encabezado
    title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Title'],
        fontSize=18,
        textColor=colors.HexColor('#1a73e8'),
        alignment=TA_CENTER,
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#333333'),
        alignment=TA_CENTER,
        spaceAfter=12
    )
    meta_style = ParagraphStyle(
        'Meta',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#666666'),
        alignment=TA_RIGHT,
        spaceAfter=10
    )

    elements.append(Paragraph('Consultorio Odontológico "Sonrisa Perfecta"', title_style))
    elements.append(Paragraph('Reporte Oficial de Citas Odontológicas', subtitle_style))

    filtro_txt = " · ".join(filtros) if filtros else "Todos los registros"
    ahora_txt = timezone.now().strftime('%d/%m/%Y %H:%M')
    elements.append(Paragraph(f'Filtros: {filtro_txt} | Generado: {ahora_txt} | Total: {citas.count()}', meta_style))
    elements.append(Spacer(1, 0.3*cm))

    # Tabla
    data = [['#', 'Paciente', 'DNI', 'Odontólogo', 'Fecha', 'Hora', 'Motivo', 'Estado']]
    for c in citas:
        data.append([
            str(c.id),
            c.paciente.nombre_completo,
            c.paciente.dni,
            c.odontologo.nombre_completo,
            c.fecha.strftime('%d/%m/%Y'),
            c.hora.strftime('%H:%M'),
            c.motivo[:35],
            c.estado,
        ])

    if len(data) == 1:
        data.append(['-', 'Sin resultados para los filtros indicados', '-', '-', '-', '-', '-', '-'])

    table = Table(data, colWidths=[1.2*cm, 5.0*cm, 2.3*cm, 5.0*cm, 2.5*cm, 2.0*cm, 6.0*cm, 2.7*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a73e8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('ALIGN', (3, 1), (3, -1), 'LEFT'),
        ('ALIGN', (6, 1), (6, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dadce0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_citas.pdf"'
    return response
