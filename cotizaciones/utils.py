#modulo de Archivo.utils encargado de la generacion de pdf 
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from io import BytesIO

def generar_pdf_cotizacion(cotizacion):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        rightMargin=50, 
        leftMargin=50,
        topMargin=40, 
        bottomMargin=40
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # ========== ENCABEZADO: EMPRESA Y LOGO ==========
    # Columna izquierda: Información de la empresa
    empresa_lines = []
    if cotizacion.empresa_nombre:
        empresa_lines.append(f"<b><font size=16>{cotizacion.empresa_nombre}</font></b>")
        empresa_lines.append("<br/>")
    
    empresa_details = []
    if cotizacion.empresa_rut:
        empresa_details.append(f"<b>RUT:</b> {cotizacion.empresa_rut}")
    if cotizacion.empresa_giro:
        empresa_details.append(f"<b>Giro:</b> {cotizacion.empresa_giro}")
    if cotizacion.empresa_direccion:
        empresa_details.append(f"<b>Dirección:</b> {cotizacion.empresa_direccion}")
    if cotizacion.empresa_telefono:
        empresa_details.append(f"<b>Teléfono:</b> {cotizacion.empresa_telefono}")
    if cotizacion.empresa_email:
        empresa_details.append(f"<b>E-mail:</b> {cotizacion.empresa_email}")
    
    empresa_lines.extend(empresa_details)
    
    empresa_style = ParagraphStyle(
        'empresa',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        alignment=TA_LEFT
    )
    empresa_para = Paragraph('<br/>'.join(empresa_lines), empresa_style)
    
    # Columna derecha: Logo y datos de cotización en caja
    right_content = []
    
    # Logo
    if getattr(cotizacion, 'logo', None):
        try:
            logo_path = cotizacion.logo.path
            logo_img = RLImage(logo_path, width=2*inch, height=1*inch)
            logo_cell = logo_img
        except Exception:
            logo_cell = Paragraph("<b>YOUR COMPANY</b><br/>Logo", 
                ParagraphStyle('logo_placeholder', parent=styles['Normal'], 
                              fontSize=10, alignment=TA_CENTER))
    else:
        logo_cell = Paragraph("<b>YOUR COMPANY</b><br/>Logo", 
            ParagraphStyle('logo_placeholder', parent=styles['Normal'], 
                          fontSize=10, alignment=TA_CENTER))
    
    # Crear caja con borde para logo
    logo_table = Table([[logo_cell]], colWidths=[2.2*inch], rowHeights=[1.1*inch])
    logo_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.grey),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    
    # Datos de cotización
    cotiz_data = []
    cotiz_data.append([Paragraph(f"<b>N° Cotización:</b> {cotizacion.numero_cotizacion}", 
                                 ParagraphStyle('cotiz1', parent=styles['Normal'], fontSize=9))])
    if cotizacion.fecha_emision:
        cotiz_data.append([Paragraph(f"<b>Fecha Emisión:</b> {cotizacion.fecha_emision.strftime('%d/%m/%Y')}", 
                                     ParagraphStyle('cotiz2', parent=styles['Normal'], fontSize=9))])
    if cotizacion.fecha_validez:
        cotiz_data.append([Paragraph(f"<b>Validez hasta °:</b> {cotizacion.fecha_validez.strftime('%d/%m/%Y')}", 
                                     ParagraphStyle('cotiz3', parent=styles['Normal'], fontSize=9))])
    
    cotiz_table = Table(cotiz_data, colWidths=[2.2*inch])
    cotiz_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'RIGHT'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    
    # Combinar logo y datos en columna derecha
    right_elements = [[logo_table], [Spacer(1, 10)], [cotiz_table]]
    right_final_table = Table(right_elements, colWidths=[2.2*inch])
    right_final_table.setStyle(TableStyle([
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    
    # Tabla principal del encabezado
    header_table = Table([[empresa_para, right_final_table]], colWidths=[4*inch, 2.5*inch])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    
    elements.append(header_table)
    elements.append(Spacer(1, 20))
    
    # ========== DATOS DEL CLIENTE ==========
    cliente_title_para = Paragraph(
        "<b>DATOS DEL CLIENTE</b>",
        ParagraphStyle('cliente_title', parent=styles['Normal'], 
                      fontSize=10, textColor=colors.white, 
                      alignment=TA_CENTER)
    )
    
    cliente_title_table = Table([[cliente_title_para]], colWidths=[6.5*inch])
    cliente_title_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#4a7bc8')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    
    # Datos del cliente en 2 columnas
    cliente_data = []
    if cotizacion.cliente:
        col1_data = []
        col2_data = []
        
        if cotizacion.cliente.nombre:
            col1_data.append(f"<b>Nombre:</b> {cotizacion.cliente.nombre}")
        if cotizacion.cliente.rut:
            col1_data.append(f"<b>RUT:</b> {cotizacion.cliente.rut}")
        if cotizacion.cliente.direccion:
            col1_data.append(f"<b>Dirección:</b> {cotizacion.cliente.direccion}")
        
        if cotizacion.cliente.email:
            col2_data.append(f"<b>Correo Electrónico:</b> {cotizacion.cliente.email}")
        if cotizacion.cliente.telefono:
            col2_data.append(f"<b>Teléfono:</b> {cotizacion.cliente.telefono}")
        
        # Balancear columnas
        while len(col2_data) < len(col1_data):
            col2_data.append('')
        
        cliente_data = [[
            Paragraph('<br/>'.join(col1_data), ParagraphStyle('cl1', parent=styles['Normal'], fontSize=9, leading=13)),
            Paragraph('<br/>'.join(col2_data), ParagraphStyle('cl2', parent=styles['Normal'], fontSize=9, leading=13))
        ]]
    else:
        cliente_data = [[
            Paragraph("Sin cliente registrado", styles['Normal']), 
            ''
        ]]
    
    cliente_content_table = Table(cliente_data, colWidths=[3.25*inch, 3.25*inch])
    cliente_content_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('BOX', (0,0), (-1,-1), 1, colors.grey),
        ('LINEABOVE', (0,0), (-1,0), 0, colors.white),
    ]))
    
    elements.append(cliente_title_table)
    elements.append(cliente_content_table)
    elements.append(Spacer(1, 20))
    
    # ========== ITEMS POR CATEGORÍA ==========
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
            # Encabezado de categoría
            cat_header_para = Paragraph(
                f"<b>{categoria.upper()}</b>", 
                ParagraphStyle('cat_h', parent=styles['Normal'], 
                              fontSize=10, textColor=colors.white)
            )
            
            cat_header_table = Table([[cat_header_para]], colWidths=[6.5*inch])
            cat_header_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#4a7bc8')),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('TOPPADDING', (0,0), (-1,-1), 5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ]))
            elements.append(cat_header_table)
            
            # Tabla de items con numeración INDEPENDIENTE por categoría
            data = [['ITEM', 'DESCRIPCIÓN', 'CANTIDAD', 'VALOR UNITARIO', 'VALOR TOTAL']]
            
            subtotal_categoria = 0
            item_number = 1  # Contador independiente por categoría
            
            for item in items_cat:
                cantidad = float(item.cantidad)
                precio_unitario = float(item.precio_unitario)
                total_item = cantidad * precio_unitario
                subtotal_categoria += total_item
                
                data.append([
                    str(item_number),  # Numeración independiente
                    item.descripcion or '',
                    str(int(cantidad)) if cantidad.is_integer() else f"{cantidad:.2f}",
                    f"${precio_unitario:,.0f}".replace(",", "."),
                    f"${total_item:,.0f}".replace(",", ".")
                ])
                item_number += 1
            
            # Fila de subtotal de categoría con diseño diferenciado
            subtotal_label = Paragraph(
                f"<b>SUBTOTAL<br/>{categoria.upper()}:</b>",
                ParagraphStyle('subtotal_label', parent=styles['Normal'], 
                              fontSize=9, alignment=TA_RIGHT)
            )
            subtotal_value = Paragraph(
                f"<b>${subtotal_categoria:,.0f}".replace(",", ".") + "</b>",
                ParagraphStyle('subtotal_value', parent=styles['Normal'], 
                              fontSize=9, alignment=TA_RIGHT)
            )
            
            data.append([
                '', '', '', 
                subtotal_label,
                subtotal_value
            ])
            
            # Crear tabla con diseño profesional
            table = Table(data, colWidths=[0.5*inch, 3*inch, 0.8*inch, 1.1*inch, 1.1*inch])
            table.setStyle(TableStyle([
                # ========== ENCABEZADO ==========
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#5b8dd6')),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('ALIGN', (0,0), (-1,0), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,0), 9),
                ('TOPPADDING', (0,0), (-1,0), 6),
                ('BOTTOMPADDING', (0,0), (-1,0), 6),
                
                # ========== ITEMS (contenido) ==========
                ('ALIGN', (0,1), (0,-2), 'CENTER'),  # ITEM centrado
                ('ALIGN', (1,1), (1,-2), 'LEFT'),    # DESCRIPCIÓN izquierda
                ('ALIGN', (2,1), (2,-2), 'CENTER'),  # CANTIDAD centrada
                ('ALIGN', (3,1), (3,-2), 'RIGHT'),   # VALOR UNITARIO derecha
                ('ALIGN', (4,1), (4,-2), 'RIGHT'),   # VALOR TOTAL derecha
                ('FONTNAME', (0,1), (-1,-2), 'Helvetica'),
                ('FONTSIZE', (0,1), (-1,-2), 9),
                ('TOPPADDING', (0,1), (-1,-2), 6),
                ('BOTTOMPADDING', (0,1), (-1,-2), 6),
                ('LEFTPADDING', (0,1), (-1,-2), 5),
                ('RIGHTPADDING', (0,1), (-1,-2), 5),
                ('BACKGROUND', (0,1), (-1,-2), colors.white),  # Fondo blanco para items
                
                # ========== SUBTOTAL DE CATEGORÍA (fila final) - DISEÑO DIFERENCIADO ==========
                ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#e8e8e8')),  # Gris claro
                ('ALIGN', (3,-1), (4,-1), 'RIGHT'),
                ('VALIGN', (3,-1), (4,-1), 'MIDDLE'),
                ('FONTNAME', (3,-1), (4,-1), 'Helvetica-Bold'),
                ('FONTSIZE', (3,-1), (4,-1), 9),
                ('TOPPADDING', (0,-1), (-1,-1), 8),
                ('BOTTOMPADDING', (0,-1), (-1,-1), 8),
                ('LEFTPADDING', (3,-1), (4,-1), 8),
                ('RIGHTPADDING', (3,-1), (4,-1), 8),
                
                # ========== BORDES Y LÍNEAS ==========
                ('BOX', (0,0), (-1,-1), 1, colors.grey),  # Borde exterior
                ('LINEBELOW', (0,0), (-1,0), 1.5, colors.HexColor('#4a7bc8')),  # Línea gruesa bajo header
                ('GRID', (0,1), (-1,-2), 0.5, colors.lightgrey),  # Grid para items (líneas sutiles)
                ('LINEABOVE', (0,-1), (-1,-1), 1.2, colors.grey),  # Línea destacada sobre subtotal
            ]))
            elements.append(table)
            elements.append(Spacer(1, 15))
    else:
        no_items = Paragraph("<i>No hay items registrados en esta cotización</i>", styles['Normal'])
        elements.append(no_items)
        elements.append(Spacer(1, 20))
    
    # ========== TÉRMINOS Y CONDICIONES / TOTALES ==========
    # Lado izquierdo: Términos y condiciones
    terminos_title = Paragraph("<b>TÉRMINOS Y CONDICIONES:</b>", 
                               ParagraphStyle('term_title', parent=styles['Normal'], 
                                            fontSize=9, spaceAfter=6))
    
    terminos_content = []
    if cotizacion.notas_adicionales:
        terminos_content.append(cotizacion.notas_adicionales)
    else:
        terminos_content.append("• Precios en pesos chilenos")
        terminos_content.append("• Valores incluyen IVA")
        terminos_content.append("• Cotización válida según fecha indicada")
    
    terminos_para = Paragraph('<br/>'.join(terminos_content), 
                             ParagraphStyle('terminos', parent=styles['Normal'], 
                                          fontSize=8, leading=12))
    
    terminos_box = [[terminos_title], [terminos_para]]
    terminos_table = Table(terminos_box, colWidths=[3.5*inch])
    terminos_table.setStyle(TableStyle([
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,1), (-1,1), 0),
    ]))
    
    # Lado derecho: Totales con diseño profesional
    subtotal = float(cotizacion.subtotal)
    iva = float(cotizacion.iva)
    total = float(cotizacion.monto_total)
    
    totales_data = [
        ['SUBTOTAL', f"${subtotal:,.0f}".replace(",", ".")],
        ['IVA    19%', f"${iva:,.0f}".replace(",", ".")],
        ['TOTAL', f"${total:,.0f}".replace(",", ".")],
    ]
    
    totales_table = Table(totales_data, colWidths=[1.3*inch, 1.4*inch])
    totales_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (0,-1), 'LEFT'),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,1), 10),
        ('FONTSIZE', (0,2), (-1,2), 12),
        
        # Colores diferenciados para cada fila
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f5f5f5')),  # Subtotal: gris muy claro
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#e8e8e8')),  # IVA: gris claro
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor('#d0d0d0')),  # Total: gris medio
        
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('BOX', (0,0), (-1,-1), 1.5, colors.grey),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.grey),  # Líneas internas
    ]))
    
    # Tabla que contiene términos y totales lado a lado
    footer_table = Table([[terminos_table, totales_table]], 
                        colWidths=[3.8*inch, 2.7*inch])
    footer_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    
    elements.append(footer_table)
    elements.append(Spacer(1, 50))
    
    # ========== FIRMAS ==========
    firma_data = [[
        Paragraph('_____________________________<br/><br/><b>Firma Emisor</b><br/><font size=8>Nombre y RUT</font>',
                 ParagraphStyle('firma1', parent=styles['Normal'], fontSize=9, alignment=TA_CENTER)),
        Paragraph('_____________________________<br/><br/><b>Firma y Timbre Cliente</b><br/><font size=8>Aceptación de la cotización</font>',
                 ParagraphStyle('firma2', parent=styles['Normal'], fontSize=9, alignment=TA_CENTER))
    ]]
    
    firma_table = Table(firma_data, colWidths=[3.25*inch, 3.25*inch])
    firma_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
    ]))
    
    elements.append(firma_table)
    
    # Construir PDF
    doc.build(elements)
    
    buffer.seek(0)
    return buffer