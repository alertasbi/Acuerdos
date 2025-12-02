from flask import Blueprint, send_file
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
import os
from datetime import datetime

pdf_template_bp = Blueprint("pdf_template", __name__)

@pdf_template_bp.post("/acuerdo-detalle")
def generar_pdf_detalle():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=20, leftMargin=20,
                            topMargin=20, bottomMargin=20)
    styles = getSampleStyleSheet()
    elements = []

    # ======== COLORES Y ESTILOS ========
    gray = colors.HexColor("#D8D9DB")
    darkgray = colors.HexColor("#4B5563")
    pink = colors.HexColor("#ED1556")
    title = ParagraphStyle("title", parent=styles["Heading2"], fontSize=12, textColor=darkgray, alignment=1)
    subtitle = ParagraphStyle("subtitle", parent=styles["Normal"], fontSize=8, textColor=darkgray, alignment=1)
    label = ParagraphStyle("label", parent=styles["Normal"], fontSize=6, textColor=darkgray)
    small = ParagraphStyle("small", parent=styles["Normal"], fontSize=5, textColor=darkgray)

    # ======== LOGO Y TÍTULO ========
    logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "Logonew_smart2.png")
    if os.path.exists(logo_path):
        # 🔹 Logo más pequeño pero más alargado (espaciado entre letras)
        logo = Image(logo_path, width=55 * mm, height=6 * mm)
    else:
        logo = Paragraph(" ", styles["Normal"])


    # --- Envolvemos el logo en una tabla angosta (para alinearlo totalmente a la izquierda) ---
    logo_table = Table([[logo]], colWidths=[60 * mm])
    logo_table.hAlign = "LEFT"  # 👈 esto es la clave
    logo_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    elements.append(logo_table)
    elements.append(Spacer(0, 0))

    # Título centrado debajo del logo
    elements.append(Paragraph("<b>ORDEN DE PUBLICIDAD</b>", title))
    #elements.append(Spacer(1, 2))

        # ======== BLOQUE 1: INFORMACIÓN DEL CLIENTE ========
    elements.append(Paragraph("INFORMACIÓN DEL CLIENTE", subtitle))
    #elements.append(Spacer(1, 0))

    # Línea rosa debajo del subtítulo
    from reportlab.lib.units import inch
    line = Table([[" "]], colWidths=[7.6 * inch], rowHeights=[0.8])
    line.hAlign = "CENTER"
    line.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), pink)
    ]))
    elements.append(line)
    #elements.append(Spacer(1, 6))

    # === Tabla izquierda ===
    # === Tabla izquierda (cliente) ===
    data_cliente_izq = [
        ["Cliente:", ""],
        ["Nombre Fiscal:", ""],
        ["Dirección Fiscal:", ""],
        ["C.P.:", ""],
    ]
    t_cliente_izq = Table(data_cliente_izq, colWidths=[80, 210])
    t_cliente_izq.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.black),
        ("BACKGROUND", (0, 0), (0, -1), gray),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))

    # === Tabla derecha (Provider Account) ===
    data_cliente_der = [
        ["Provider Account:", ""],
        ["ID:", ""],
        ["R.F.C.:", ""],
        ["Comprobante:", ""],
    ]
    t_cliente_der = Table(data_cliente_der, colWidths=[90, 120])
    t_cliente_der.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.black),
        ("BACKGROUND", (0, 0), (0, -1), gray),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))

    # === Contenedor general (alineación igual que la tabla de contactos) ===
    tablas_cliente = Table([[t_cliente_izq, "", t_cliente_der]], colWidths=[290, 10, 200])
    elements.append(tablas_cliente)
    elements.append(Spacer(1, 3))


        # ======== BLOQUE 2: CONTACTOS DEL CLIENTE ========
    elements.append(Paragraph("CONTACTOS DEL CLIENTE", subtitle))
    elements.append(Table([[" "]], colWidths=[520], rowHeights=[0.8],
                          style=[("BACKGROUND", (0, 0), (-1, -1), pink)]))

    # Línea rosa debajo del subtítulo
    from reportlab.lib.units import inch


    # Titulos fuera de las tablas
    titulos_contacto = Table([
        [Paragraph("<b>Contacto Contabilidad</b>", subtitle), "", Paragraph("<b>Contacto Marketing</b>", subtitle)]
    ], colWidths=[250, 20, 250])
    titulos_contacto.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER")
    ]))
    elements.append(titulos_contacto)


    # === Tabla izquierda (Contabilidad) ===
    data_contabilidad = [
        ["Nombre:", ""],
        ["Cargo:", ""],
        ["E-mail:", ""],
        ["Teléfono:", ""],
    ]
    t_contabilidad = Table(data_contabilidad, colWidths=[80, 170])
    t_contabilidad.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.black),
        ("BACKGROUND", (0, 0), (0, -1), gray),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))

    # === Tabla derecha (Marketing) ===
    data_marketing = [
        ["Nombre:", ""],
        ["Cargo:", ""],
        ["E-mail:", ""],
        ["Teléfono:", ""],
    ]
    t_marketing = Table(data_marketing, colWidths=[80, 170])
    t_marketing.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.black),
        ("BACKGROUND", (0, 0), (0, -1), gray),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))

    # === Contenedor con separación entre ambas ===
    tablas_contactos = Table([[t_contabilidad, "", t_marketing]], colWidths=[250, 20, 250])
    tablas_contactos.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    elements.append(tablas_contactos)
    elements.append(Spacer(1, 3))


    # ======== BLOQUE 3: DETALLES PUBLICIDAD CONTRATADA / DESGLOSE ========

    # --- Titulos individuales alineados arriba de cada tabla ---
    titulos_detalle = Table([
        [
            Paragraph("DETALLES PUBLICIDAD CONTRATADA", subtitle),
            "",
            Paragraph("DESGLOSE DE PUBLICIDAD CONTRATADA", subtitle)
        ]
    ], colWidths=[250, 20, 250])
    titulos_detalle.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
    ]))
    elements.append(titulos_detalle)

    # --- Línea rosa debajo de los títulos ---
    lineas = Table(
        [["", "", ""]],
        colWidths=[250, 20, 250],
        rowHeights=[0.8]
    )
    lineas.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (0, 0), 0.8, pink),  # línea izquierda
        ("LINEBELOW", (2, 0), (2, 0), 0.8, pink),  # línea derecha
    ]))
    elements.append(lineas)
    elements.append(Spacer(1, 2))

    # === Tabla izquierda: DETALLES PUBLICIDAD CONTRATADA ===
    data_detalles = [
        ["Área:", ""],
        ["Moneda:", ""],
        ["Fechas del Plan:", ""],
        ["Núm. Facturas:", ""],
        ["Fechas de Facturación:", ""],
    ]
    t_detalles = Table(data_detalles, colWidths=[80, 170])
    t_detalles.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.black),
        ("BACKGROUND", (0, 0), (0, -1), gray),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))

    # === Tabla derecha: DESGLOSE DE PUBLICIDAD CONTRATADA ===
    data_desglose = [
        ["Pauta Acciones Varias", ""],
        ["Subtotal:", ""],
        ["IVA 19%:", ""],
        ["TOTAL COP - Peso colombiano:", ""],
    ]
    t_desglose = Table(data_desglose, colWidths=[150, 90])
    t_desglose.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.black),
        ("BACKGROUND", (0, 1), (0, -1), gray),
        ("BACKGROUND", (0, 0), (0, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))

    # === Contenedor general (alineado como los bloques anteriores) ===
    tablas_detalle = Table([[t_detalles, "", t_desglose]], colWidths=[250, 20, 250])
    tablas_detalle.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    elements.append(tablas_detalle)
    #elements.append(Spacer(1, 3))




    # ======== BLOQUE 4: OBSERVACIONES / COMENTARIOS ========
    #elements.append(Spacer(1, 8))

    # Contenedor del bloque completo (alineado con las tablas)
    bloque_obs = []

    # Título
    bloque_obs.append(Paragraph("<b>OBSERVACIONES / COMENTARIOS</b>", subtitle))
    #bloque_obs.append(Spacer(1, 2))

    # Línea rosa — mismo ancho y posición que las tablas
    linea_obs = Table([[" "]], colWidths=[270], rowHeights=[0.8])
    linea_obs.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), pink),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    bloque_obs.append(linea_obs)
    bloque_obs.append(Spacer(1, 4))

    # Cuadro gris (mismo ancho que la línea y tablas)
    cuadro_obs = Table(
        [[""]],  # sin puntos
        colWidths=[270],
        rowHeights=[50]  # altura del recuadro gris
    )
    cuadro_obs.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), gray),
        ("BOX", (0, 0), (-1, -1), 0.5, gray),
    ]))
    bloque_obs.append(cuadro_obs)

    # Envolvemos todo para alinearlo perfectamente con las tablas
    bloque_obs_wrap = Table([[bloque_obs]], colWidths=[270])
    bloque_obs_wrap.hAlign = "LEFT"
    bloque_obs_wrap.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 15),  # ⬅️ margen ajustado exacto a las tablas
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    elements.append(bloque_obs_wrap)
    #elements.append(Spacer(1, 12))




        # ======== BLOQUE 5: FORMA DE PAGO ========
    #elements.append(Spacer(1, 8))

    # Contenedor del bloque completo alineado igual que las tablas
    bloque_pago = []

    # Título
    bloque_pago.append(Paragraph("<b>FORMA DE PAGO</b>", subtitle))
    #bloque_pago.append(Spacer(1, 2))

    # Línea rosa delgada (alineada igual que las tablas)
    linea_pago = Table([[" "]], colWidths=[270], rowHeights=[0.8])
    linea_pago.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), pink),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    bloque_pago.append(linea_pago)
    #bloque_pago.append(Spacer(1, 4))

    # Texto descriptivo
    texto_forma_pago = (
        "El monto total con <b>IVA incluido</b> será descontado directamente de la siguiente "
        "facturación por producción de PriceTravel dentro de la vigencia de la publicidad contratada."
    )

    # 🔹 Estilo sin espacio entre líneas
    sin_interlineado = ParagraphStyle(
        "sin_interlineado",
        parent=small,
        leading=small.fontSize,  # igual al tamaño de letra (sin espacio extra)
    )

    # Tabla principal: columna izquierda (gris + rosa) y derecha (texto)
    t_pago = Table([
        [
            Paragraph("<b><font color='#ED1556'>Descuento</font></b>", label),
            Paragraph(texto_forma_pago, sin_interlineado)
        ]
    ], colWidths=[85, 185])
    t_pago.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), gray),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TEXTCOLOR", (1, 0), (1, 0), darkgray),
        ("FONTSIZE", (1, 0), (1, 0), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    bloque_pago.append(t_pago)

    # Envolver todo para mantener alineación con las tablas
    bloque_pago_wrap = Table([[bloque_pago]], colWidths=[270])
    bloque_pago_wrap.hAlign = "LEFT"
    bloque_pago_wrap.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 15),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ])) 
    elements.append(bloque_pago_wrap)
    #elements.append(Spacer(1, 12))


    # ======== BLOQUE 6: INFORMACIÓN BANCARIA ========
    elements.append(Paragraph("<b>INFORMACIÓN BANCARIA</b>", subtitle))

    # Línea rosa delgada (mismo ancho que el resto del documento)
    from reportlab.lib.units import inch
    linea_bancos = Table([[" "]], colWidths=[7.6 * inch], rowHeights=[0.8])
    linea_bancos.hAlign = "CENTER"
    linea_bancos.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), pink),
    ]))
    elements.append(linea_bancos)

    # Base de logos
    base_assets = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
    bancos = [
        {
            "logo": os.path.join(base_assets, "bancomer_logo.jpg"),
            "cuentas": [
                "Bancomer - Cuenta en Pesos Mexicanos: Cuenta 0174262662 Clave 012691001742626627",
                "Bancomer - Cuenta en Dólares Americanos: Cuenta 0174455142 Clave 012691001744551428 SWIFT: BCMRMXMMXXX",
            ],
        },
        {
            "logo": os.path.join(base_assets, "santander_logo.png"),
            "cuentas": [
                "Santander - Cuenta en Pesos Mexicanos: Cuenta 65502674134 Clave 014691655026741342",
                "Santander - Cuenta en Dólares Americanos: Cuenta 82500504024 Clave 014691825005040247 SWIFT: BMSXMXMMXXX",
            ],
        },
        {
            "logo": os.path.join(base_assets, "banorte_logo.png"),
            "cuentas": [
                "Banorte - Cuenta en Pesos Mexicanos: Cuenta 0646673673 Clave 072691006466736731",
                "Banorte - Cuenta en Dólares Americanos: Cuenta 0642079549 Clave 072691006420795491 SWIFT: MENOMXMTXXX",
            ],
        },
                {
            "logo": os.path.join(base_assets, "bancolombia_logo.png"),
            "cuentas": [
                "Bancolombia - Cuenta en Pesos Colombianos  :  Cuenta 82543776725   Corriente",
                "Bancolombia - Cuenta en Dólares Americano :    Cuenta 82543776725   Corriente  SWIFT: COLOCOBM",
            ],
        },
    ]

    # 🔹 Estilo sin interlineado (dentro del mismo banco)
    sin_interlineado_banco = ParagraphStyle(
        "sin_interlineado_banco",
        parent=small,
        leading=small.fontSize,  # sin espacio entre líneas
    )

    # Contenedor general para alinear el bloque completo a la izquierda
    bloque_bancos = []
    for banco in bancos:
        # --- Ajustar tamaño del logo según el banco ---
        if os.path.exists(banco["logo"]):
            if "bancolombia" in banco["logo"].lower():
                # Logo más ancho (Bancolombia)
                logo = Image(banco["logo"], width=20 * mm, height=6 * mm)
            else:
                # Logos normales
                logo = Image(banco["logo"], width=7 * mm, height=7 * mm)
        else:
            logo = Paragraph(" ", styles["Normal"])

        # Crear párrafo sin interlineado
        cuentas_texto = "<br/>".join(banco["cuentas"])
        texto = Paragraph(cuentas_texto, sin_interlineado_banco)

        # Fila tabla
        fila = Table(
            [[logo, texto]],
            colWidths=[22 * mm, 380]   # ← Aumentamos espacio para logo de Bancolombia
        )
        fila.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
        ]))

        bloque_bancos.append(fila)
        bloque_bancos.append(Spacer(1, 3))


    # 🔹 Envolver el bloque con el mismo margen que las demás secciones
    bloque_bancos_wrap = Table([[bloque_bancos]], colWidths=[440])
    bloque_bancos_wrap.hAlign = "LEFT"
    bloque_bancos_wrap.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 15),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    elements.append(bloque_bancos_wrap)

    #elements.append(Spacer(1, 10))



    # ======== BLOQUE 7: FIRMAS ========
    #elements.append(Spacer(1, 20))

    # Encabezados principales
    titulos_firmas = Table(
        [[
            Paragraph("<b>PRICETRAVEL HOLDING</b>", subtitle),
            Paragraph("<b>CLIENTE</b>", subtitle)
        ]],
        colWidths=[250, 250]
    )
    titulos_firmas.hAlign = "CENTER"
    titulos_firmas.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    elements.append(titulos_firmas)

    # === Fecha en español ===
    meses = {
        "January": "enero", "February": "febrero", "March": "marzo",
        "April": "abril", "May": "mayo", "June": "junio",
        "July": "julio", "August": "agosto", "September": "septiembre",
        "October": "octubre", "November": "noviembre", "December": "diciembre"
    }
    fecha_actual = datetime.now().strftime("%d %B %Y")
    for en, es in meses.items():
        fecha_actual = fecha_actual.replace(en, es)

    # === Datos de la tabla ===
    data_firmas = [
        ["Nombre:", Paragraph("<b>""</b>", small), "Nombre:", ""],
        ["Firma:", "", "Firma:", ""],
        ["Fecha:", Paragraph("<b>""</b>", small), "Fecha:", ""],
    ]

    # === Tabla con más aire visual ===
    t_firmas = Table(data_firmas, colWidths=[70, 180, 70, 180], rowHeights=[22, 22, 22])  # 🔹 Más espacio entre renglones
    t_firmas.hAlign = "CENTER"
    t_firmas.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (-1, -1), darkgray),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),

        # 🔹 Líneas negras finas, limpias y de la misma longitud
        ("LINEBELOW", (1, 0), (1, 2), 1.2, colors.black),
        ("LINEBELOW", (3, 0), (3, 2), 1.2, colors.black),

        # 🔹 Espaciado preciso: encabezado ligeramente separado de la línea
        ("TOPPADDING", (0, 0), (-1, -1), 3),     # más aire sobre el texto
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),  # altura entre líneas ajustada

        # 🔹 Sin bordes ni grids
        ("BOX", (0, 0), (-1, -1), 0, colors.white),
        ("INNERGRID", (0, 0), (-1, -1), 0, colors.white),
    ]))
    elements.append(t_firmas)
    elements.append(Spacer(1, 15))





    # ======== BLOQUE 8: FOOTER FINAL ========

    # --- Logo más pequeño, más ancho (separación de letras) ---
    logo_footer_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "Logonew_smart2.png")
    if os.path.exists(logo_footer_path):
        logo_footer = Image(logo_footer_path, width=28 * mm, height=4 * mm)  # 🔹 más pequeño y estirado
    else:
        logo_footer = Paragraph("PriceTravel", subtitle)

    # Logo centrado con espacio debajo
    logo_footer_table = Table([[logo_footer]], colWidths=[60 * mm])
    logo_footer_table.hAlign = "CENTER"
    logo_footer_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),  # 🔹 más espacio entre logo y texto
    ]))
    elements.append(Spacer(1, 4))
    elements.append(logo_footer_table)
    elements.append(Spacer(1, 2))

    # --- Texto legal extendido y compacto ---
    footer_text = (
        "<b>9000642360</b> facilitará a PriceTravel Holding cuanto material gráfico sea necesario para la ejecución de los diferentes medios publicitarios contemplados en la campaña de publicidad, "
        "asimismo <b>9000642360</b> se hace responsable de que las imágenes, derechos de imagen o de autor, fotografías, material gráfico, textos publicitarios que se entreguen a PriceTravel Holding "
        "para su inclusión en folletos o su difusión por cualquier otro medio y en este acto deslinda a PriceTravel Holding de cualquier responsabilidad derivada de su falta de actualización, inexactitud o veracidad."
    )

    footer_style = ParagraphStyle(
        "footer",
        parent=styles["Normal"],
        fontSize=5,          # 🔹 más pequeño
        textColor=darkgray,
        alignment=1,         # centrado
        leading=6,           # 🔹 sin espacio extra entre líneas
        spaceBefore=0,
        spaceAfter=0,
    )

    # --- Footer extendido (más ancho, como en el ejemplo) ---
    footer_paragraph = Paragraph(footer_text, footer_style)
    footer_table = Table([[footer_paragraph]], colWidths=[520])  # 🔹 más ancho que antes (abarca más horizontalmente)
    footer_table.hAlign = "CENTER"
    footer_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))

    elements.append(footer_table)

    # ======== GENERAR PDF ========
    doc.build(elements)
    buffer.seek(0)
    return send_file(buffer, mimetype="application/pdf",
                     download_name="acuerdo_detalle.pdf", as_attachment=False)
