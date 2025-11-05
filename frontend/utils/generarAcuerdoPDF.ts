// utils/generarAcuerdoPDF.ts
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'

export const generarAcuerdoPDF = async (form: any, hoteles: any[]) => {
  const doc = new jsPDF('p', 'mm', 'letter')
  const pink = [237, 21, 86]
  const grayText = [75, 75, 75]
  const grayLight = [216, 217, 219]
  const grayMedium = [190, 192, 194]
  const pageWidth = doc.internal.pageSize.getWidth()

  // =====================================================
  // 🔹 LOGO + ENCABEZADO
  // =====================================================
  try {
    const logo = new Image()
    logo.src = '/images/Logonew_smart2.png'
    doc.addImage(logo, 'PNG', 25, 15, 45, 25)
  } catch {
    console.warn('⚠️ Logo no encontrado, continúa sin imagen.')
  }

  doc.setFont('helvetica', 'bold')
  doc.setFontSize(16)
  doc.setTextColor(...grayText)
  doc.text('ORDEN DE PUBLICIDAD', pageWidth / 2, 28, { align: 'center' })
  doc.setDrawColor(...pink)
  doc.setLineWidth(0.8)
  doc.line(25, 32, pageWidth - 25, 32)

  // =====================================================
  // 🧾 INFORMACIÓN DEL CLIENTE
  // =====================================================
  doc.setFontSize(11)
  doc.setTextColor(...grayText)
  autoTable(doc, {
    startY: 40,
    theme: 'grid',
    styles: {
      font: 'helvetica',
      fontSize: 8,
      textColor: grayText,
      lineColor: grayMedium,
      cellPadding: 2
    },
    head: [['INFORMACIÓN DEL CLIENTE']],
    headStyles: {
      fillColor: [255, 255, 255],
      textColor: grayText,
      halign: 'center',
      fontSize: 10,
      fontStyle: 'bold',
      lineColor: pink,
      lineWidth: 0.8
    },
    body: [
      ['Cliente:', form.clienteRFC || '—', '', 'Provider Account:', '—'],
      ['Nombre Fiscal:', '—', '', 'ID:', '—'],
      ['Dirección Fiscal:', '—', '', 'R.F.C.:', form.clienteRFC || '—'],
      ['C.P.:', '—', '', 'Comprobante:', form.comprobante || '—']
    ],
    bodyStyles: { fillColor: [255, 255, 255] },
    columnStyles: {
      0: { fillColor: grayLight, fontStyle: 'bold' },
      3: { fillColor: grayLight, fontStyle: 'bold' }
    }
  })

  // =====================================================
  // 👥 CONTACTOS DEL CLIENTE
  // =====================================================
  autoTable(doc, {
    startY: (doc as any).lastAutoTable.finalY + 6,
    theme: 'grid',
    styles: { font: 'helvetica', fontSize: 8, textColor: grayText, lineColor: grayMedium, cellPadding: 2 },
    head: [['CONTACTOS DEL CLIENTE']],
    headStyles: {
      fillColor: [255, 255, 255],
      textColor: grayText,
      halign: 'center',
      fontSize: 10,
      fontStyle: 'bold',
      lineColor: pink,
      lineWidth: 0.8
    },
    body: [
      ['Contacto Contabilidad', '', 'Contacto Marketing'],
      ['Nombre:', form.contabilidadNombre || '—', 'Nombre:', form.marketingNombre || '—'],
      ['Cargo:', form.contabilidadCargo || '—', 'Cargo:', form.marketingCargo || '—'],
      ['E-mail:', form.contabilidadEmail || '—', 'E-mail:', form.marketingEmail || '—'],
      ['Teléfono:', form.contabilidadTelefono || '—', 'Teléfono:', form.marketingTelefono || '—']
    ],
    columnStyles: {
      0: { fillColor: grayLight, fontStyle: 'bold' },
      2: { fillColor: grayLight, fontStyle: 'bold' }
    }
  })

  // =====================================================
  // 📊 DETALLES PUBLICIDAD CONTRATADA
  // =====================================================
  autoTable(doc, {
    startY: (doc as any).lastAutoTable.finalY + 8,
    theme: 'grid',
    styles: { font: 'helvetica', fontSize: 8, textColor: grayText, lineColor: grayMedium, cellPadding: 2 },
    head: [['DETALLES PUBLICIDAD CONTRATADA']],
    headStyles: {
      fillColor: [255, 255, 255],
      textColor: grayText,
      halign: 'center',
      fontSize: 10,
      fontStyle: 'bold',
      lineColor: pink,
      lineWidth: 0.8
    },
    body: [
      ['Área:', form.equipo || '—', '', 'Moneda:', form.moneda || '—'],
      ['Precio sin IVA:', `${form.precioSinIVA || '—'} ${form.moneda}`, '', 'IVA:', `${form.iva || 0}%`],
      ['Total:', `${Number(form.precioSinIVA || 0) * (1 + Number(form.iva || 0) / 100)} ${form.moneda}`, '', 'Forma de pago:', form.formaPago || '—'],
      ['Fechas del Plan:', `${form.fechaInicio || ''} - ${form.fechaTermino || ''}`, '', 'Número de Factura:', form.numeroFactura || '—']
    ],
    columnStyles: {
      0: { fillColor: grayLight, fontStyle: 'bold' },
      3: { fillColor: grayLight, fontStyle: 'bold' }
    }
  })

  // =====================================================
  // 💬 OBSERVACIONES / COMENTARIOS
  // =====================================================
  autoTable(doc, {
    startY: (doc as any).lastAutoTable.finalY + 8,
    theme: 'plain',
    styles: { font: 'helvetica', fontSize: 8, textColor: grayText, cellPadding: 3 },
    head: [['OBSERVACIONES / COMENTARIOS']],
    headStyles: {
      fillColor: [255, 255, 255],
      textColor: grayText,
      halign: 'center',
      fontSize: 10,
      fontStyle: 'bold',
      lineColor: pink,
      lineWidth: 0.8
    },
    body: [[form.comentarios || 'Sin comentarios.']],
    bodyStyles: { fillColor: grayLight }
  })

  // =====================================================
  // 💳 FORMA DE PAGO
  // =====================================================
  autoTable(doc, {
    startY: (doc as any).lastAutoTable.finalY + 8,
    theme: 'grid',
    styles: { font: 'helvetica', fontSize: 9, textColor: grayText, lineColor: grayMedium },
    head: [['FORMA DE PAGO']],
    headStyles: {
      fillColor: [255, 255, 255],
      textColor: grayText,
      halign: 'center',
      fontSize: 10,
      fontStyle: 'bold',
      lineColor: pink,
      lineWidth: 0.8
    },
    body: [[form.formaPago || '—']],
    bodyStyles: { fillColor: grayLight, halign: 'center', fontStyle: 'bold', textColor: pink }
  })

  // =====================================================
  // 🏦 INFORMACIÓN BANCARIA
  // =====================================================
  autoTable(doc, {
    startY: (doc as any).lastAutoTable.finalY + 12,
    theme: 'grid',
    styles: { font: 'helvetica', fontSize: 8, textColor: grayText, lineColor: grayMedium, cellPadding: 2 },
    head: [['INFORMACIÓN BANCARIA']],
    headStyles: {
      fillColor: [255, 255, 255],
      textColor: grayText,
      halign: 'center',
      fontSize: 10,
      fontStyle: 'bold',
      lineColor: pink,
      lineWidth: 0.8
    },
    body: [
      ['Banco BBVA', 'Cuenta: 1234-5678-9012\nCLABE: 001122334455667788\nTitular: PriceTravel Holding'],
      ['Banco Santander', 'Cuenta: 9988-7766-5544\nCLABE: 112233445566778899\nTitular: PriceTravel Holding'],
      ['Banco Banorte', 'Cuenta: 4455-6677-8899\nCLABE: 998877665544332211\nTitular: PriceTravel Holding']
    ],
    columnStyles: {
      0: { fillColor: grayLight, fontStyle: 'bold', cellWidth: 45 },
      1: { cellWidth: 125 }
    }
  })

  // =====================================================
  // 🖋️ FIRMAS
  // =====================================================
  const yStart = (doc as any).lastAutoTable.finalY + 20
  doc.setDrawColor(grayMedium[0], grayMedium[1], grayMedium[2])
  doc.line(40, yStart, 90, yStart)
  doc.line(130, yStart, 180, yStart)
  doc.setFontSize(9)
  doc.text('PRICETRAVEL HOLDING', 45, yStart + 5)
  doc.text('CLIENTE', 145, yStart + 5)

  const fecha = new Date()
  doc.setFontSize(8)
  doc.text(`Fecha: ${fecha.toLocaleDateString('es-MX', {
    day: '2-digit',
    month: 'long',
    year: 'numeric'
  })}`, 40, yStart + 18)

  // =====================================================
  // 🦶 FOOTER
  // =====================================================
  doc.setFontSize(7)
  doc.setTextColor(100)
  doc.text(
    'Documento generado automáticamente por el sistema de acuerdos PriceTravel Holding.',
    25,
    270
  )

  // =====================================================
  // 📦 EXPORT
  // =====================================================
  const pdfArrayBuffer = doc.output('arraybuffer')
  const pdfBlob = new Blob([pdfArrayBuffer], { type: 'application/pdf' })
  return pdfBlob
}
