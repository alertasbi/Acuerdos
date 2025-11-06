from flask import Blueprint, request, send_file, jsonify
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os

pdf_bp = Blueprint("pdf", __name__)

@pdf_bp.post("/acuerdo")
def generar_pdf_acuerdo():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se recibieron datos"}), 400

        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=40, leftMargin=40,
            topMargin=60, bottomMargin=40
        )
        styles = getSampleStyleSheet()
        elements = []

        # --- Encabezado con logo (opcional) ---
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "Logonew_smart2.png")
        if os.path.exists(logo_path):
            elements.append(Image(logo_path, width=120, height=35))
            elements.append(Spacer(1, 8))

        title = Paragraph("ORDEN DE PUBLICIDAD", styles["Heading2"])
        elements.append(title)
        elements.append(Spacer(1, 12))

        # --- Tabla de datos generales ---
        def val(k, default="—"):
            v = data.get(k)
            return default if v in (None, "", []) else v

        datos = [
            ["Cliente / RFC",     val("clienteRFC")],
            ["Equipo",            val("equipo")],
            ["Tipo de acuerdo",   val("tipoAcuerdo")],
            ["Folio Media",       val("folioMedia")],
            ["Moneda",            val("moneda")],
            ["Precio sin IVA",    f'{val("precioSinIVA","—")} {val("moneda","")}'],
            ["IVA",               f'{val("iva","—")} %' if val("iva","") != "—" else "—"],
            ["Forma de pago",     val("formaPago")],
            ["Fechas",            f'{val("fechaInicio")} al {val("fechaTermino")}'],
            ["Comentarios",       val("comentarios")],
        ]

        tabla = Table(datos, colWidths=[150, 300])
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F3F4F6")),
            ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#D1D5DB")),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#E5E7EB")),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ]))
        elements.append(tabla)
        elements.append(Spacer(1, 16))

        # --- Hoteles seleccionados ---
        hoteles = data.get("hoteles", [])
        if hoteles:
            elements.append(Paragraph("<b>Hoteles seleccionados</b>", styles["Normal"]))
            table_data = [["ID Hotel", "Nombre Hotel"]] + [[h.get("id",""), h.get("nombre","")] for h in hoteles]
            t = Table(table_data, colWidths=[100, 350])
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EAEAEA")),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D1D5DB")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
            ]))
            elements.append(Spacer(1, 6))
            elements.append(t)
            elements.append(Spacer(1, 16))

        # --- Firmas ---
        elements.append(Spacer(1, 28))
        firmas = [
            ["_________________________", "_________________________"],
            ["PRICETRAVEL HOLDING",   "CLIENTE"],
        ]
        firmas_tabla = Table(firmas, colWidths=[250, 250])
        firmas_tabla.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica-Bold"),
        ]))
        elements.append(firmas_tabla)

        # --- Pie ---
        elements.append(Spacer(1, 24))
        elements.append(Paragraph(
            "Documento generado automáticamente por el sistema de acuerdos — PriceTravel Holding",
            styles["Normal"]
        ))

        # Generar PDF
        doc.build(elements)
        buffer.seek(0)
        return send_file(buffer, mimetype="application/pdf", download_name="acuerdo.pdf", as_attachment=False)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
