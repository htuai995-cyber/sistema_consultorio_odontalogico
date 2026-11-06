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
from gestion.models import Receta
from gestion.forms import RecetaForm


@login_required
def receta_lista(request):
    q = request.GET.get('q', '')
    fecha = request.GET.get('fecha', '')
    recetas = Receta.objects.select_related('diagnostico__cita__paciente', 'diagnostico__cita__odontologo').all()

    if q:
        recetas = recetas.filter(
            medicamento__icontains=q) | Receta.objects.filter(
            diagnostico__cita__paciente__nombres__icontains=q) | Receta.objects.filter(
            diagnostico__cita__paciente__apellidos__icontains=q)
    if fecha:
        recetas = recetas.filter(fecha_emision=fecha)

    recetas = recetas.distinct().order_by('-fecha_emision', '-id')
    paginator = Paginator(recetas, 10)
    page = request.GET.get('page')
    recetas_page = paginator.get_page(page)

    return render(request, 'gestion/receta/lista.html', {
        'recetas': recetas_page,
        'q': q,
        'fecha': fecha,
        'total_registros': recetas.count(),
        'titulo': 'Recetas Médicas',
    })


@login_required
def receta_crear(request):
    if request.method == 'POST':
        form = RecetaForm(request.POST)
        if form.is_valid():
            rec = form.save()
            messages.success(request, f'Receta #{rec.id} registrada exitosamente.')
            return redirect('receta_lista')
    else:
        form = RecetaForm()
    return render(request, 'gestion/receta/form.html', {
        'form': form,
        'titulo': 'Nueva Receta',
        'accion': 'Registrar',
    })


@login_required
def receta_editar(request, pk):
    receta = get_object_or_404(Receta, pk=pk)
    if request.method == 'POST':
        form = RecetaForm(request.POST, instance=receta)
        if form.is_valid():
            form.save()
            messages.success(request, f'Receta #{pk} actualizada exitosamente.')
            return redirect('receta_lista')
    else:
        form = RecetaForm(instance=receta)
    return render(request, 'gestion/receta/form.html', {
        'form': form,
        'titulo': f'Editar Receta #{receta.id}',
        'accion': 'Actualizar',
        'objeto': receta,
    })


@login_required
def receta_eliminar(request, pk):
    receta = get_object_or_404(Receta, pk=pk)
    if request.method == 'POST':
        receta.delete()
        messages.success(request, f'Receta #{pk} eliminada exitosamente.')
        return redirect('receta_lista')
    return render(request, 'gestion/confirmar_eliminar.html', {
        'objeto': receta,
        'titulo': 'Eliminar Receta',
        'cancelar_url': 'receta_lista',
    })


@login_required
def receta_reporte_pdf(request):
    q = request.GET.get('q', '')
    fecha = request.GET.get('fecha', '')
    recetas = Receta.objects.select_related('diagnostico__cita__paciente', 'diagnostico__cita__odontologo').all()
    filtros = []

    if q:
        recetas = recetas.filter(
            medicamento__icontains=q) | Receta.objects.filter(
            diagnostico__cita__paciente__nombres__icontains=q) | Receta.objects.filter(
            diagnostico__cita__paciente__apellidos__icontains=q)
        filtros.append(f'Búsqueda: "{q}"')
    if fecha:
        recetas = recetas.filter(fecha_emision=fecha)
        filtros.append(f'Fecha Emisión: {fecha}')

    recetas = recetas.distinct().order_by('-fecha_emision', '-id')

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
    elements.append(Paragraph('Reporte Oficial de Recetas Odontológicas', subtitle_style))

    filtro_txt = " · ".join(filtros) if filtros else "Todos los registros"
    ahora_txt = timezone.now().strftime('%d/%m/%Y %H:%M')
    elements.append(Paragraph(f'Filtros: {filtro_txt} | Generado: {ahora_txt} | Total: {recetas.count()}', meta_style))
    elements.append(Spacer(1, 0.3*cm))

    data = [['#', 'Paciente', 'Medicamento', 'Dosis', 'Frecuencia', 'Duración', 'Indicaciones', 'Fecha']]
    for r in recetas:
        data.append([
            str(r.id),
            r.diagnostico.cita.paciente.nombre_completo,
            r.medicamento,
            r.dosis,
            r.frecuencia,
            r.duracion,
            r.indicaciones[:35],
            r.fecha_emision.strftime('%d/%m/%Y'),
        ])

    if len(data) == 1:
        data.append(['-', 'Sin resultados para los filtros indicados', '-', '-', '-', '-', '-', '-'])

    table = Table(data, colWidths=[1.2*cm, 5.0*cm, 4.5*cm, 2.5*cm, 3.2*cm, 2.3*cm, 4.5*cm, 2.5*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a73e8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('ALIGN', (2, 1), (2, -1), 'LEFT'),
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
    response['Content-Disposition'] = 'inline; filename="reporte_recetas.pdf"'
    return response
