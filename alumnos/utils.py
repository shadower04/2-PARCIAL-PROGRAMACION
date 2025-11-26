import os
from io import BytesIO
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from django.core.mail import EmailMessage
from datetime import datetime

def generar_pdf_alumno(alumno):
    """Genera un PDF con los datos del alumno"""
    buffer = BytesIO()
    
    # Crear el documento PDF
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Contenido del PDF
    contenido = []
    
    # Título
    titulo_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Centrado
    )
    contenido.append(Paragraph("Ficha del Alumno", titulo_style))
    
    # Datos del alumno
    datos = [
        ['Nombre:', f"{alumno.nombre} {alumno.apellido}"],
        ['Email:', alumno.email],
        ['Edad:', str(alumno.edad)],
        ['Teléfono:', alumno.telefono],
        ['Dirección:', alumno.direccion],
        ['Estado:', alumno.get_estado_display()],
        ['Fecha de registro:', alumno.fecha_creacion.strftime("%d/%m/%Y %H:%M")],
    ]
    
    # Crear tabla
    tabla = Table(datos, colWidths=[100, 300])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.grey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    contenido.append(tabla)
    contenido.append(Spacer(1, 20))
    
    # Pie de página
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    pie = Paragraph(f"Generado el {fecha} - Sistema de Alumnos", styles['Normal'])
    contenido.append(pie)
    
    # Construir PDF
    doc.build(contenido)
    
    buffer.seek(0)
    return buffer

def enviar_pdf_email(destinatario, pdf_buffer, alumno):
    """Envía el PDF por email"""
    subject = f'Ficha del Alumno - {alumno.nombre} {alumno.apellido}'
    message = f'''
    Hola,
    
    Adjuntamos la ficha del alumno {alumno.nombre} {alumno.apellido}.
    
    Este documento fue generado automáticamente por el sistema.
    
    Saludos,
    Sistema de Gestión de Alumnos
    '''
    
    email = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [destinatario],
    )
    
    # Adjuntar PDF
    email.attach(
        f'alumno_{alumno.nombre}_{alumno.apellido}.pdf',
        pdf_buffer.getvalue(),
        'application/pdf'
    )
    
    email.send()