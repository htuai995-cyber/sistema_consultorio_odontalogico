from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from reportlab.lib.pagesizes import A5
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import io
from gestion.models import Receta, Cita, Diagnostico, Tratamiento, Paciente


@login_required
def reportes_centro(request):
    """Centro unificado de reportes del consultorio."""
    hoy = timezone.now().date()
    total_citas = Cita.objects.count()
    total_diagnosticos = Diagnostico.objects.count()
    total_tratamientos = Tratamiento.objects.count()
    total_recetas = Receta.objects.count()

    return render(request, 'gestion/reportes/index.html', {
        'titulo': 'Centro de Reportes',
        'hoy': hoy,
        'total_citas': total_citas,
        'total_diagnosticos': total_diagnosticos,
        'total_tratamientos': total_tratamientos,
        'total_recetas': total_recetas,
    })


@login_required
def receta_individual_pdf(request, pk):
    """Genera la receta médica oficial individual para entregar al paciente."""
    receta = get_object_or_404(
        Receta.objects.select_related(
            'diagnostico__cita__paciente',
            'diagnostico__cita__odontologo__especialidad'
        ),
        pk=pk
    )

    paciente = receta.diagnostico.cita.paciente
    odontologo = receta.diagnostico.cita.odontologo

    buffer = io.BytesIO()
    # Formato A5 vertical (ideal para recetas médicas)
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A5,
        leftMargin=1.5*cm,
        rightMargin=1.5*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm
    )

    styles = getSampleStyleSheet()
    elements = []

    # Membrete institucional
    title_style = ParagraphStyle(
        'ClinicTitle',
        parent=styles['Title'],
        fontSize=15,
        textColor=colors.HexColor('#1a73e8'),
        alignment=TA_CENTER,
        spaceAfter=2
    )
    clinic_sub = ParagraphStyle(
        'ClinicSub',
        parent=styles['Normal'],
        fontSize=8.5,
        textColor=colors.HexColor('#5f6368'),
        alignment=TA_CENTER,
        spaceAfter=8
    )

    elements.append(Paragraph('CONSULTORIO ODONTOLÓGICO "SONRISA PERFECTA"', title_style))
    elements.append(Paragraph('Salud Bucal & Estética Dental Integral · RUC: 20489512341<br/>Av. Larco 456, Miraflores · Teléf.: (01) 445-8920', clinic_sub))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1a73e8'), spaceAfter=10))

    # Título de documento
    receta_title = ParagraphStyle(
        'RecetaTitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#202124'),
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        spaceAfter=10
    )
    elements.append(Paragraph(f'RECETA MÉDICA N.º {receta.id:06d}', receta_title))

    # Datos del paciente y médico
    info_data = [
        [
            Paragraph(f'<b>Paciente:</b> {paciente.nombre_completo}', styles['Normal']),
            Paragraph(f'<b>DNI:</b> {paciente.dni}', styles['Normal']),
        ],
        [
            Paragraph(f'<b>Médico Tratante:</b> {odontologo.nombre_completo}', styles['Normal']),
            Paragraph(f'<b>N.º Colegiatura:</b> {odontologo.numero_colegiatura}', styles['Normal']),
        ],
        [
            Paragraph(f'<b>Especialidad:</b> {odontologo.especialidad.nombre}', styles['Normal']),
            Paragraph(f'<b>Fecha de Emisión:</b> {receta.fecha_emision.strftime("%d/%m/%Y")}', styles['Normal']),
        ]
    ]

    info_table = Table(info_data, colWidths=[7.0*cm, 4.5*cm])
    info_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LINEBELOW', (0, -1), (-1, -1), 0.5, colors.HexColor('#dadce0')),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.4*cm))

    # Prescripción (Rp/)
    rp_style = ParagraphStyle(
        'RpStyle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#1a73e8'),
        fontName='Helvetica-Bold',
        spaceAfter=6
    )
    elements.append(Paragraph('Rp. /', rp_style))

    med_data = [
        [Paragraph('<b>Medicamento Indicado</b>', styles['Normal']), Paragraph(receta.medicamento, styles['Normal'])],
        [Paragraph('<b>Dosis</b>', styles['Normal']), Paragraph(receta.dosis, styles['Normal'])],
        [Paragraph('<b>Frecuencia</b>', styles['Normal']), Paragraph(receta.frecuencia, styles['Normal'])],
        [Paragraph('<b>Duración</b>', styles['Normal']), Paragraph(receta.duracion, styles['Normal'])],
        [Paragraph('<b>Indicaciones / Posología</b>', styles['Normal']), Paragraph(receta.indicaciones or 'Seguir pauta indicada por el especialista.', styles['Normal'])],
    ]

    med_table = Table(med_data, colWidths=[4.2*cm, 7.3*cm])
    med_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#202124')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dadce0')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
    ]))
    elements.append(med_table)
    elements.append(Spacer(1, 1.2*cm))

    # Firma y sello
    firma_data = [
        ['', '_______________________________________'],
        ['', f'{odontologo.nombre_completo}'],
        ['', f'{odontologo.especialidad.nombre} · COP: {odontologo.numero_colegiatura}'],
        ['', 'Firma y Sello del Odontólogo'],
    ]
    firma_table = Table(firma_data, colWidths=[4.5*cm, 7.0*cm])
    firma_table.setStyle(TableStyle([
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('FONTSIZE', (1, 0), (1, -1), 7.5),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#5f6368')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
    ]))
    elements.append(firma_table)

    doc.build(elements)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="receta_{receta.id}_{paciente.dni}.pdf"'
    return response

