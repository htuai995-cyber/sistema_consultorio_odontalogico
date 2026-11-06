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
from gestion.models import Tratamiento
from gestion.forms import TratamientoForm


@login_required
def tratamiento_lista(request):
    q = request.GET.get('q', '')
    estado = request.GET.get('estado', '')
    fecha = request.GET.get('fecha', '')
    tratamientos = Tratamiento.objects.select_related('diagnostico__cita__paciente', 'diagnostico__cita__odontologo').all()

    if q:
        tratamientos = tratamientos.filter(
            nombre__icontains=q) | Tratamiento.objects.filter(
            diagnostico__cita__paciente__nombres__icontains=q) | Tratamiento.objects.filter(
            diagnostico__cita__paciente__apellidos__icontains=q)
    if estado:
        tratamientos = tratamientos.filter(estado=estado)
    if fecha:
        tratamientos = tratamientos.filter(fecha_inicio=fecha)

    tratamientos = tratamientos.distinct().order_by('-fecha_inicio', '-id')
    paginator = Paginator(tratamientos, 10)
    page = request.GET.get('page')
    tratamientos_page = paginator.get_page(page)

    return render(request, 'gestion/tratamiento/lista.html', {
        'tratamientos': tratamientos_page,
        'q': q,
        'estado': estado,
        'fecha': fecha,
        'total_registros': tratamientos.count(),
        'titulo': 'Tratamientos',
        'estados': ['Pendiente', 'En proceso', 'Finalizado'],
    })


@login_required
def tratamiento_crear(request):
    if request.method == 'POST':
        form = TratamientoForm(request.POST)
        if form.is_valid():
            trat = form.save()
            messages.success(request, f'Tratamiento "{trat.nombre}" registrado exitosamente.')
            return redirect('tratamiento_lista')
    else:
        form = TratamientoForm()
    return render(request, 'gestion/tratamiento/form.html', {
        'form': form,
        'titulo': 'Nuevo Tratamiento',
        'accion': 'Registrar',
    })


@login_required
def tratamiento_editar(request, pk):
    tratamiento = get_object_or_404(Tratamiento, pk=pk)
    if request.method == 'POST':
        form = TratamientoForm(request.POST, instance=tratamiento)
        if form.is_valid():
            form.save()
            messages.success(request, f'Tratamiento "{tratamiento.nombre}" actualizado exitosamente.')
            return redirect('tratamiento_lista')
    else:
        form = TratamientoForm(instance=tratamiento)
    return render(request, 'gestion/tratamiento/form.html', {
        'form': form,
        'titulo': f'Editar Tratamiento #{tratamiento.id}',
        'accion': 'Actualizar',
        'objeto': tratamiento,
    })


@login_required
def tratamiento_eliminar(request, pk):
    tratamiento = get_object_or_404(Tratamiento, pk=pk)
    if request.method == 'POST':
        tratamiento.delete()
        messages.success(request, f'Tratamiento #{pk} eliminado.')
        return redirect('tratamiento_lista')
    return render(request, 'gestion/confirmar_eliminar.html', {
        'objeto': tratamiento,
        'titulo': 'Eliminar Tratamiento',
        'cancelar_url': 'tratamiento_lista',
    })


@login_required
def tratamiento_reporte_pdf(request):
    q = request.GET.get('q', '')
    estado = request.GET.get('estado', '')
    fecha = request.GET.get('fecha', '')
    tratamientos = Tratamiento.objects.select_related('diagnostico__cita__paciente', 'diagnostico__cita__odontologo').all()
    filtros = []

    if q:
        tratamientos = tratamientos.filter(
            nombre__icontains=q) | Tratamiento.objects.filter(
            diagnostico__cita__paciente__nombres__icontains=q) | Tratamiento.objects.filter(
            diagnostico__cita__paciente__apellidos__icontains=q)
        filtros.append(f'Búsqueda: "{q}"')
    if estado:
        tratamientos = tratamientos.filter(estado=estado)
        filtros.append(f'Estado: {estado}')
    if fecha:
        tratamientos = tratamientos.filter(fecha_inicio=fecha)
        filtros.append(f'Fecha Inicio: {fecha}')

    tratamientos = tratamientos.distinct().order_by('-fecha_inicio', '-id')

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
    elements.append(Paragraph('Reporte Oficial de Tratamientos Odontológicos', subtitle_style))

    filtro_txt = " · ".join(filtros) if filtros else "Todos los registros"
    ahora_txt = timezone.now().strftime('%d/%m/%Y %H:%M')
    elements.append(Paragraph(f'Filtros: {filtro_txt} | Generado: {ahora_txt} | Total: {tratamientos.count()}', meta_style))
    elements.append(Spacer(1, 0.3*cm))

    data = [['#', 'Tratamiento', 'Paciente', 'F. Inicio', 'F. Fin', 'Costo', 'Estado']]
    total_costo = 0
    for t in tratamientos:
        total_costo += t.costo
        data.append([
            str(t.id),
            t.nombre,
            t.diagnostico.cita.paciente.nombre_completo,
            t.fecha_inicio.strftime('%d/%m/%Y'),
            t.fecha_fin.strftime('%d/%m/%Y'),
            f'S/. {t.costo:,.2f}',
            t.estado,
        ])

    if len(data) == 1:
        data.append(['-', 'Sin resultados para los filtros indicados', '-', '-', '-', '-', '-'])
    else:
        data.append(['', 'TOTAL COSTO', '', '', '', f'S/. {total_costo:,.2f}', ''])

    table = Table(data, colWidths=[1.2*cm, 6.5*cm, 6.0*cm, 2.7*cm, 2.7*cm, 3.5*cm, 3.1*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a73e8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('ALIGN', (2, 1), (2, -1), 'LEFT'),
        ('ALIGN', (5, 1), (5, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dadce0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2 if len(data) > 2 else -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    if len(data) > 2:
        table.setStyle(TableStyle([
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8f0fe')),
        ]))
    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_tratamientos.pdf"'
    return response
