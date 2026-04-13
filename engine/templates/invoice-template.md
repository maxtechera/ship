# Invoice Template — Uruguayan Format

> **Template version:** 1.0 | Ship Engine GTM Deliverable  
> Formato conforme a requisitos DGI (Dirección General Impositiva) — Uruguay

---

## FACTURA / REMITO

---

**Empresa Emisora**

| Campo | Valor |
|-------|-------|
| **Razón Social** | `[Tu Empresa S.R.L. / Unipersonal]` |
| **RUT** | `[XX-XXXXXX-X-X]` |
| **Domicilio Fiscal** | `[Dirección completa, Ciudad, Uruguay]` |
| **Teléfono** | `[+598 XX XXX XXX]` |
| **Email** | `[facturacion@empresa.com]` |
| **Actividad** | `[Descripción de la actividad CIIU]` |

---

**Datos del Documento**

| Campo | Valor |
|-------|-------|
| **Tipo de Documento** | Factura / e-Factura / Ticket |
| **Número** | `Nº XXXX-XXXXXXX` |
| **Serie** | `[A / B / E]` |
| **Fecha de Emisión** | `DD/MM/YYYY` |
| **Fecha de Vencimiento** | `DD/MM/YYYY` |
| **Moneda** | UYU (Pesos Uruguayos) / USD |

---

**Cliente (Receptor)**

| Campo | Valor |
|-------|-------|
| **Razón Social / Nombre** | |
| **RUT / CI** | |
| **Domicilio** | |
| **Email** | |
| **País** | Uruguay / `[otro país]` |

---

## Detalle de Servicios / Productos

| # | Descripción | Cantidad | Precio Unitario | Subtotal |
|---|-------------|----------|-----------------|----------|
| 1 | `[Descripción del servicio/producto]` | 1 | $ | $ |
| 2 | `[...]` | | | $ |
| 3 | `[...]` | | | $ |

---

## Totales

| Concepto | Monto |
|----------|-------|
| **Subtotal (sin impuestos)** | $ |
| **IVA 22%** (servicios generales) | $ |
| **IVA 10%** (si aplica — mínimo básico) | $ |
| **IRAE retenido** (si aplica — 12%) | − $ |
| **IRPF retenido** (si aplica) | − $ |
| **TOTAL A PAGAR** | **$** |

> **Nota IVA:** Tasa general 22%. Tasa mínima 10% (alimentos, medicamentos, etc.).  
> Si eres **pequeña empresa** o **monotributo**, indica "No Incluye IVA" si corresponde.

---

## Condiciones de Pago

| Campo | Valor |
|-------|-------|
| **Forma de pago** | Transferencia bancaria / Efectivo / Cheque / Débito |
| **Plazo** | Contado / 30 días / 60 días |
| **Banco** | `[Nombre del banco]` |
| **Cuenta corriente Nº** | `[XXXXXXXX]` |
| **BROU / ITAÚ / Santander / HSBC** | `[según corresponda]` |

---

## Información Adicional (opcional)

- **Orden de compra Nº:** 
- **Proyecto / Referencia:**
- **Período de servicio:**
- **Notas:**

---

## Para Servicios Digitales / SaaS (exportación)

> Si facturas a clientes en el exterior:

| Campo | Valor |
|-------|-------|
| **Tipo** | Exportación de servicios |
| **IVA** | Exento (Art. 34 Tít. 10 TO 1996) |
| **Moneda** | USD / EUR |
| **Leyenda** | "Servicio exportado. Exento de IVA." |

---

## Datos para e-Factura (DGI)

Si emites **e-Factura electrónica** (CFE):

- **Proveedor DGI autorizado:** (Uruware, EFactura.uy, AFIP, etc.)
- **Código de Seguridad** (QR / CAF): `[generado por software]`
- **Firma digital:** Incluida en CFE
- **Formato:** XML (envío a DGI) + PDF (envío a cliente)
- **Constancia de recepción DGI:** Adjuntar a archivos

---

## Checklist Emisión

- [ ] RUT emisor correcto y vigente
- [ ] RUT / CI receptor completo
- [ ] Número de factura correlativo
- [ ] Descripción clara del servicio
- [ ] IVA calculado correctamente (22% o 10%)
- [ ] Retenciones aplicadas si aplica (IRAE, IRPF)
- [ ] Fecha de vencimiento indicada
- [ ] Firmado (físico o digital CFE)
- [ ] Copia archivo (papel / sistema)

---

## Recursos DGI Uruguay

- Portal DGI: [dgi.gub.uy](https://www.dgi.gub.uy)
- Consulta RUT: [servicios.dgi.gub.uy/serviciosenlinea](https://servicios.dgi.gub.uy)
- Resolución CFE: DGI Resolución 798/012

---

_Template: Ship Engine · NEO-231_
