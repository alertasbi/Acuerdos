// utils/generarAcuerdoPDF.ts
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'

export const generarAcuerdoPDF = (form: any, hoteles: any[]) => {
  const doc = new jsPDF('p', 'mm', 'a4')

  // 🔹 Encabezado
  doc.setFontSize(16)
  doc.text('ORDEN DE PUBLICIDAD', 105, 20, { align: 'center' })
  doc.setFontSize(11)

  // 🔹 Datos principales
  doc.text(`Cliente/RFC: ${form.clienteRFC || ''}`, 20, 40)
  doc.text(`Equipo: ${form.equipo || ''}`, 20, 48)
  doc.text(`Tipo de acuerdo: ${form.tipoAcuerdo || ''}`, 20, 56)
  doc.text(`Moneda: ${form.moneda || ''}`, 20, 64)
  doc.text(`Precio sin IVA: ${form.precioSinIVA || ''}`, 20, 72)
  doc.text(`IVA: ${form.iva || ''}%`, 20, 80)
  doc.text(`Forma de pago: ${form.formaPago || ''}`, 20, 88)
  doc.text(`Fechas: ${form.fechaInicio} - ${form.fechaTermino}`, 20, 96)

  // 🔹 Hoteles seleccionados
  if (hoteles && hoteles.length > 0) {
    autoTable(doc, {
      startY: 110,
      head: [['ID Hotel', 'Nombre Hotel']],
      body: hoteles.map((h) => [h.id, h.nombre]),
    })
  }

  // 🔹 Espacio para firmas
  const y = doc.lastAutoTable ? doc.lastAutoTable.finalY + 20 : 200
  doc.text('______________________________', 40, y)
  doc.text('PRICETRAVEL HOLDING', 45, y + 6)
  doc.text('______________________________', 130, y)
  doc.text('CLIENTE', 150, y + 6)

  // 🔹 Guardar PDF
  doc.save(`Orden_Publicidad_${form.clienteRFC || 'acuerdo'}.pdf`)
}
