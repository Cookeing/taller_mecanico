#modulo de Archivo.utils encargado de la generacion de pdf 
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from io import BytesIO

def generar_pdf_cotizacion(cotizacion):

#funcion main donde se define al estrutura y margen espesifico de el pdf
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        rightMargin=72, 
        leftMargin=72,
        topMargin=72, 
        bottomMargin=18
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
#Estilo simple del titulo 
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=1  # Centrado
    )
    
    # ======================================= ENCABEZADO ==============================================
    title = Paragraph("COTIZACIÓN", title_style)
    elements.append(title)
    
    # verifica emediante un bloque de cotiacion la Información de la empresa
    if cotizacion.empresa_nombre:
        empresa_data = [
            ['EMPRESA:', cotizacion.empresa_nombre],
            ['RUT:', cotizacion.empresa_rut or ''],
            ['GIRO:', cotizacion.empresa_giro or ''],
            ['DIRECCIÓN:', cotizacion.empresa_direccion or ''],
            ['TELÉFONO:', cotizacion.empresa_telefono or ''],
            ['EMAIL:', cotizacion.empresa_email or ''],
        ]
        
        empresa_table = Table(empresa_data, colWidths=[1.5*inch, 4*inch])
        empresa_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        elements.append(empresa_table)
        elements.append(Spacer(1, 20))
    
#======================================== ========== INFORMACIÓN DE LA COTIZACIÓN ============================
    info_data = [
        ['N° COTIZACIÓN:', cotizacion.numero_cotizacion],
        ['FECHA EMISIÓN:', cotizacion.fecha_emision.strftime('%d/%m/%Y')],
    ]
    
    if cotizacion.fecha_validez:
        info_data.append(['VÁLIDA HASTA:', cotizacion.fecha_validez.strftime('%d/%m/%Y')])
    
    info_data.append(['', ''])
    
    # Información del cliente
    if cotizacion.cliente:
        info_data.append(['CLIENTE:', cotizacion.cliente.nombre])
        if cotizacion.cliente.rut:
            info_data.append(['RUT CLIENTE:', cotizacion.cliente.rut])
        if cotizacion.cliente.direccion:
            info_data.append(['DIRECCIÓN:', cotizacion.cliente.direccion])
        if cotizacion.cliente.telefono:
            info_data.append(['TELÉFONO:', cotizacion.cliente.telefono])
        if cotizacion.cliente.email:
            info_data.append(['EMAIL:', cotizacion.cliente.email])
    else:
        info_data.append(['CLIENTE:', 'Sin cliente registrado'])
    
    # Información del servicio vinculado
    if cotizacion.servicio:
        info_data.append(['', ''])
        info_data.append(['SERVICIO VINCULADO:', f"Servicio #{cotizacion.servicio.id}"])
        if cotizacion.servicio.vehiculo:
            vehiculo_info = f"{cotizacion.servicio.vehiculo.patente} - {cotizacion.servicio.vehiculo.marca} {cotizacion.servicio.vehiculo.modelo}"
            info_data.append(['VEHÍCULO:', vehiculo_info])
        if cotizacion.servicio.descripcion_trabajo:
            descripcion = cotizacion.servicio.descripcion_trabajo[:100] + '...' if len(cotizacion.servicio.descripcion_trabajo) > 100 else cotizacion.servicio.descripcion_trabajo
            info_data.append(['DESCRIPCIÓN:', descripcion])
    
    info_table = Table(info_data, colWidths=[1.5*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 30))
    
    # ========== ITEMS/CATEGORÍAS ==========
    items = cotizacion.items.all().order_by('categoria', 'id')
    
    if items.exists():
        # Agrupar por categoría
        categorias = {}
        for item in items:
            cat = item.categoria or 'Sin categoría'
            if cat not in categorias:
                categorias[cat] = []
            categorias[cat].append(item)
        
        # Crear tabla por cada categoría
        for categoria, items_cat in categorias.items():
            # Título de categoría
            cat_title = Paragraph(f"<b>{categoria}</b>", styles['Heading2'])
            elements.append(cat_title)
            elements.append(Spacer(1, 10))
            
            # Datos de la tabla
            data = [['DESCRIPCIÓN', 'CANT.', 'PRECIO UNIT.', 'TOTAL']]
            
            for item in items_cat:
                cantidad = float(item.cantidad)
                precio_unitario = float(item.precio_unitario)
                total_item = cantidad * precio_unitario
                
                data.append([
                    item.descripcion,
                    str(int(cantidad)) if cantidad.is_integer() else f"{cantidad:.2f}",
                    f"${precio_unitario:,.0f}",
                    f"${total_item:,.0f}"
                ])
            
            # Crear tabla
            table = Table(data, colWidths=[3*inch, 0.8*inch, 1.2*inch, 1.2*inch])
            table.setStyle(TableStyle([
                # Encabezado
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                
                # Contenido
                ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
                ('ALIGN', (0, 1), (0, -1), 'LEFT'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('TOPPADDING', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
                
                # Bordes
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#2980b9')),
            ]))
            elements.append(table)
            elements.append(Spacer(1, 20))
    else:
        no_items = Paragraph("<i>No hay items registrados en esta cotización</i>", styles['Normal'])
        elements.append(no_items)
        elements.append(Spacer(1, 20))
    
    # ========== TOTALES ==========
    subtotal = float(cotizacion.subtotal)
    iva = float(cotizacion.iva)
    total = float(cotizacion.monto_total)
    
    totales_data = [
        ['SUBTOTAL (Neto):', f"${subtotal:,.0f}"],
        ['IVA (19%):', f"${iva:,.0f}"],
        ['TOTAL:', f"${total:,.0f}"],
    ]
    
    totales_table = Table(totales_data, colWidths=[4.3*inch, 1.9*inch])
    totales_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 1), 'Helvetica'),
        ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 1), 10),
        ('FONTSIZE', (0, 2), (-1, 2), 12),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#2ecc71')),
        ('TEXTCOLOR', (0, 2), (-1, 2), colors.whitesmoke),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    elements.append(totales_table)
    elements.append(Spacer(1, 30))
    
    # ========== CONDICIONES DE PAGO ==========
    if cotizacion.forma_pago or cotizacion.plazo_pago:
        pago_title = Paragraph("<b>Condiciones de Pago</b>", styles['Heading3'])
        elements.append(pago_title)
        elements.append(Spacer(1, 10))
        
        pago_data = []
        if cotizacion.forma_pago:
            pago_data.append(['Forma de pago:', cotizacion.get_forma_pago_display()])
        if cotizacion.plazo_pago:
            pago_data.append(['Plazo de pago:', cotizacion.get_plazo_pago_display()])
        
        pago_table = Table(pago_data, colWidths=[2*inch, 4.2*inch])
        pago_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        elements.append(pago_table)
        elements.append(Spacer(1, 20))
    
    # ========== ESTADO DE LA COTIZACIÓN ==========
    estado_color = {
        'PENDIENTE': colors.HexColor('#f39c12'),
        'APROBADA': colors.HexColor('#27ae60'),
        'RECHAZADA': colors.HexColor('#e74c3c'),
    }
    
    estado_data = [[f'Estado: {cotizacion.get_estado_cotizacion_display()}']]
    estado_table = Table(estado_data, colWidths=[6.2*inch])
    estado_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), estado_color.get(cotizacion.estado_cotizacion, colors.grey)),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(estado_table)
    
    # ========== PIE DE PÁGINA ==========
    elements.append(Spacer(1, 30))
    footer_text = f"<i>Documento generado el {cotizacion.fecha_creacion.strftime('%d/%m/%Y %H:%M')}</i>"
    footer = Paragraph(footer_text, styles['Normal'])
    elements.append(footer)
    
    # Construir PDF
    doc.build(elements)
    
    buffer.seek(0)
    return buffer