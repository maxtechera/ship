# Prompt: Generate Invoice (Uruguayan Format)

> Use with: Ship Engine engine · Stage: Finance / Operations

---

## System Context

You are a bilingual business assistant familiar with Uruguayan tax regulations (DGI) helping a founder generate a compliant invoice.

---

## Prompt

```
Generate a complete invoice in Uruguayan format (DGI-compliant) based on the following details.

**Emisor (Sender):**
- Razón Social / Nombre: {{razon_social}}
- RUT: {{rut}}
- Domicilio fiscal: {{domicilio}}
- Email de facturación: {{email_facturacion}}
- Actividad / CIIU: {{actividad}}

**Receptor (Client):**
- Nombre / Razón Social: {{nombre_cliente}}
- RUT / CI: {{rut_cliente}}
- Domicilio: {{domicilio_cliente}}
- Email: {{email_cliente}}
- País: {{pais_cliente}}

**Documento:**
- Tipo: {{tipo_documento}} (Factura / e-Factura / Ticket)
- Serie: {{serie}} (A / B / E)
- Número: {{numero}}
- Fecha de emisión: {{fecha}}
- Moneda: {{moneda}} (UYU / USD)

**Servicios:**
{{servicios}}
(Format: "1. [Description] — Qty: X — Unit price: $Y" per line)

**Impuestos:**
- IVA rate: {{iva_rate}} (22% standard, 10% minimum, 0% export)
- ¿Es exportación de servicios?: {{es_exportacion}} (sí/no)
- Retenciones: {{retenciones}} (IRAE 12% / IRPF / ninguna)

**Condiciones de pago:**
- Forma de pago: {{forma_pago}}
- Banco y cuenta: {{banco_cuenta}}

**Output format:**
Generate a clean, formatted invoice document ready to send:
1. Header with all sender details
2. Invoice number and dates
3. Client details
4. Itemized service table with subtotals
5. Tax calculations (IVA, retenciones)
6. Total to pay
7. Payment instructions
8. Legal footer (DGI compliance note)

If it's an export of services, note "Exento de IVA — Art. 34 Tít. 10 TO 1996".
Output in Spanish. Make it professional and ready to send as-is.
```

---

## Variables to Replace

| Variable | Description | Example |
|----------|-------------|---------|
| `{{razon_social}}` | Your company name | "MaxTech Solutions S.R.L." |
| `{{rut}}` | Your RUT number | "21-123456-0-1" |
| `{{domicilio}}` | Your fiscal address | "Av. 18 de Julio 1234, Montevideo" |
| `{{servicios}}` | List of services with qty and price | "1. Desarrollo web — 1 — $5,000" |
| `{{iva_rate}}` | IVA rate to apply | "22%" |
| `{{es_exportacion}}` | Exporting to foreign client? | "sí" |

---

_Prompt: Ship Engine · NEO-231_


---
**Bilingual Output (MANDATORY per Decision #9):** Generate full output in English (EN) first, then generate the complete output again in Spanish (ES-419 Latin American Spanish). Use VoC language adapted authentically for each language — do NOT machine-translate. Label each section: `[EN]` and `[ES]`.
