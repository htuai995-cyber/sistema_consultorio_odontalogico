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
from gestion.models import Diagnostico
from gestion.forms import DiagnosticoForm


@login_required
def diagnostico_lista(request):
    q = request.GET.get('q', '')
    fecha = request.GET.get('fecha', '')
    diagnosticos = Diagnostico.objects.select_related('cita__paciente', 'cita__odontologo').all()

    if q:
        diagnosticos = diagnosticos.filter(
            cita__paciente__nombres__icontains=q) | Diagnostico.objects.filter(
            cita__paciente__apellidos__icontains=q) | Diagnostico.objects.filter(
            descripcion__icontains=q)
    if fecha:
        diagnosticos = diagnosticos.filter(fecha=fecha)

    diagnosticos = diagnosticos.distinct().order_by('-fecha', '-id')
    paginator = Paginator(diagnosticos, 10)
    page = request.GET.get('page')
    diagnosticos_page = paginator.get_page(page)

    return render(request, 'gestion/diagnostico/lista.html', {
        'diagnosticos': diagnosticos_page,
        'q': q,
        'fecha': fecha,
        'total_registros': diagnosticos.count(),
        'titulo': 'Diagnósticos',
    })


@login_required
def diagnostico_crear(request):
    if request.method == 'POST':
        form = DiagnosticoForm(request.POST)
        if form.is_valid():
            diag = form.save()
            messages.success(request, f'Diagnóstico #{diag.id} registrado exitosamente.')
            return redirect('diagnostico_lista')
    else:
        form = DiagnosticoForm()
    return render(request, 'gestion/diagnostico/form.html', {
        'form': form,
        'titulo': 'Nuevo Diagnóstico',
        'accion': 'Registrar',
    })


@login_required
def diagnostico_editar(request, pk):
    diagnostico = get_object_or_404(Diagnostico, pk=pk)
    if request.method == 'POST':
        form = DiagnosticoForm(request.POST, instance=diagnostico)
        if form.is_valid():
            form.save()
            messages.success(request, f'Diagnóstico #{pk} actualizado exitosamente.')
            return redirect('diagnostico_lista')
    else:
        form = DiagnosticoForm(instance=diagnostico)
    return render(request, 'gestion/diagnostico/form.html', {
        'form': form,
        'titulo': f'Editar Diagnóstico #{diagnostico.id}',
        'accion': 'Actualizar',
        'objeto': diagnostico,
    })


@login_required
def diagnostico_eliminar(request, pk):
    diagnostico = get_object_or_404(Diagnostico, pk=pk)
    if request.method == 'POST':
        try:
            diagnostico.delete()
            messages.success(request, f'Diagnóstico #{pk} eliminado.')
        except Exception:
            messages.error(request, 'No se puede eliminar: tiene tratamientos o recetas asociadas.')
        return redirect('diagnostico_lista')
    return render(request, 'gestion/confirmar_eliminar.html', {
        'objeto': diagnostico,
        'titulo': 'Eliminar Diagnóstico',
        'cancelar_url': 'diagnostico_lista',
    })


@login_required
def diagnostico_reporte_pdf(request):
    q = request.GET.get('q', '')
    fecha = request.GET.get('fecha', '')
    diagnosticos = Diagnostico.objects.select_related('cita__paciente', 'cita__odontologo').all()
    filtros = []

    if q:
        diagnosticos = diagnosticos.filter(
            cita__paciente__nombres__icontains=q) | Diagnostico.objects.filter(
            cita__paciente__apellidos__icontains=q) | Diagnostico.objects.filter(
            descripcion__icontains=q)
        filtros.append(f'Búsqueda: "{q}"')
    if fecha:
        diagnosticos = diagnosticos.filter(fecha=fecha)
        filtros.append(f'Fecha: {fecha}')

    diagnosticos = diagnosticos.distinct().order_by('-fecha', '-id')

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
    elements.append(Paragraph('Reporte Oficial de Diagnósticos Clínicos', subtitle_style))

    filtro_txt = " · ".join(filtros) if filtros else "Todos los registros"
    ahora_txt = timezone.now().strftime('%d/%m/%Y %H:%M')
    elements.append(Paragraph(f'Filtros: {filtro_txt} | Generado: {ahora_txt} | Total: {diagnosticos.count()}', meta_style))
    elements.append(Spacer(1, 0.3*cm))

    data = [['#', 'Paciente', 'Odontólogo', 'Fecha', 'Diagnóstico Clínico', 'Recomendaciones']]
    for d in diagnosticos:
        data.append([
            str(d.id),
            d.cita.paciente.nombre_completo,
            d.cita.odontologo.nombre_completo,
            d.fecha.strftime('%d/%m/%Y'),
            d.descripcion[:55],
            d.recomendaciones[:55],
        ])

    if len(data) == 1:
        data.append(['-', 'Sin resultados para los filtros indicados', '-', '-', '-', '-'])

    table = Table(data, colWidths=[1.2*cm, 5.2*cm, 5.0*cm, 2.5*cm, 6.5*cm, 6.3*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a73e8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('ALIGN', (2, 1), (2, -1), 'LEFT'),
        ('ALIGN', (4, 1), (4, -1), 'LEFT'),
        ('ALIGN', (5, 1), (5, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dadce0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_diagnosticos.pdf"'
    return response
