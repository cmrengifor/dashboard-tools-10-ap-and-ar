# Dashboard 04 — Receivables Collection Dashboard

## Objetivo

Monitoreo del estado de cobranza de cuentas por cobrar: identificar facturas vencidas por antigüedad (DPD buckets), medir la tasa de colección y el saldo pendiente por segmento de cliente y estado de pago, para priorizar acciones de cobranza y reducir el ciclo de cobro.

---

## KPIs

| KPI | Descripción |
|---|---|
| **Total AR Outstanding** | Saldo total pendiente de cobro en todas las facturas activas |
| **Collection Rate** | % del monto facturado efectivamente cobrado |
| **% Overdue** | % de facturas con días de vencimiento > 0 |
| **Avg Days Outstanding** | Promedio de días que lleva pendiente una factura sin pagar |

---

## Dataset

**Archivo:** `data/receivables_data.csv`
**Filas:** 845 registros
**Generado con:** `data/generate_data.py`

### Columnas

| Columna | Tipo | Descripción |
|---|---|---|
| invoice_id | String | ID único de factura (RCV-0001 … RCV-0845) |
| customer_id | String | ID del cliente (CUST-001 … CUST-050) |
| customer_name | String | Nombre del cliente |
| customer_segment | String | Enterprise, Government, Retail, SMB |
| region | String | North, South, East, West, Central |
| sales_rep | String | Nombre del representante de ventas |
| collector | String | Nombre del responsable de cobranza |
| invoice_date | Date | Fecha de emisión de la factura |
| due_date | Date | Fecha de vencimiento |
| payment_terms | Integer | Días de crédito (15, 30, 60, 90) |
| invoice_amount | Decimal | Monto total facturado |
| paid_amount | Decimal | Monto cobrado |
| outstanding_balance | Decimal | Saldo pendiente (invoice_amount − paid_amount) |
| payment_date | Date | Fecha de pago (vacío si pendiente) |
| days_outstanding | Integer | Días transcurridos desde la fecha de emisión |
| days_overdue | Integer | Días vencidos sobre la fecha límite |
| payment_status | String | Current / Overdue / Paid / Partial |
| collection_status | String | Current / 1-30 DPD / 31-60 DPD / 61-90 DPD / 90+ DPD |
| payment_method | String | Wire / Check / Credit Card / ACH |
| promise_to_pay_date | Date | Fecha de compromiso de pago del cliente |
| last_contact_date | Date | Último contacto con el cliente |

### Distribución de datos

| collection_status | Registros |
|---|---|
| 90+ DPD | 212 |
| Current | 201 |
| 1-30 DPD | 164 |
| 31-60 DPD | 138 |
| 61-90 DPD | 130 |
| **Total** | **845** |

| payment_status | Registros |
|---|---|
| Paid | 540 |
| Current | 137 |
| Overdue | 87 |
| Partial | 81 |

| customer_segment | Registros |
|---|---|
| Retail | 246 |
| Enterprise | 232 |
| SMB | 238 |
| Government | 129 |

- **Total AR Outstanding:** $15,977,651
- **Facturas vencidas (DPD > 0):** 644 de 845

---

## Visualizaciones (Power BI)

| # | Visual | Tipo | Campos |
|---|---|---|---|
| 1 | Outstanding by Collection Status | Column Chart | collection_status (X-axis) / outstanding_balance (Y-axis) |
| 2 | Outstanding by Customer Segment | Column Chart | customer_segment (X-axis) / outstanding_balance (Y-axis) |
| 3 | Customer Balance Detail | Table | customer_name / Sum of outstanding_balance / collection_status |
| 4 | Payment Status Distribution | Donut Chart | payment_status (Legend) / outstanding_balance (Values) |
| 5 | Total AR Outstanding | KPI | Total AR Outstanding (measure) |
| 6 | Collection Rate | KPI | Collection Rate (measure) |
| 7 | % Overdue | KPI | % Overdue (measure) |
| 8 | Avg Days Outstanding | KPI | Avg Days Outstanding (measure) |
| 9 | Filter: customer_segment | Slicer | customer_segment |
| 10 | Filter: region | Slicer | region |
| 11 | Filter: sales_rep | Slicer | sales_rep |
| 12 | Filter: collection_status | Slicer | collection_status |

### Medidas DAX

| Medida | Descripción |
|---|---|
| `Total AR Outstanding` | `SUM(receivables_data[outstanding_balance])` |
| `Collection Rate` | `DIVIDE(SUM(paid_amount), SUM(invoice_amount))` |
| `% Overdue` | `DIVIDE(COUNTROWS overdue invoices, COUNTROWS all invoices)` |
| `Avg Days Outstanding` | `AVERAGEX(outstanding invoices, days_outstanding)` |

---

## Estructura del archivo PBIX

```
receivables_collection_dashboard.pbix
├── Page 1
│   ├── KPI: Total AR Outstanding
│   ├── KPI: Collection Rate
│   ├── KPI: % Overdue
│   ├── KPI: Avg Days Outstanding
│   ├── Column Chart: outstanding_balance by collection_status
│   ├── Column Chart: outstanding_balance by customer_segment
│   ├── Table: customer_name | outstanding_balance | collection_status
│   ├── Donut Chart: outstanding_balance by payment_status
│   ├── Slicer: customer_segment
│   ├── Slicer: region
│   ├── Slicer: sales_rep
│   └── Slicer: collection_status
└── DataModel
    └── receivables_data (845 filas, 21 columnas)
```

---

## Instrucciones de uso

1. Abrir `receivables_collection_dashboard.pbix` en **Power BI Desktop** (versión 2024+).
2. La página **Page 1** muestra los 4 KPIs de cobranza y todos los visuales de distribución.
3. Usar los **slicers** para filtrar por segmento de cliente, región, representante de ventas o antigüedad de deuda (DPD).
4. Para actualizar datos reales:
   - Reemplazar `data/receivables_data.csv` con exportación del sistema ERP/AR.
   - Mantener los mismos nombres de columna.
   - En Power BI Desktop: **Home → Refresh**.

---

*Dashboard generado el 07/06/2026. Parte del portafolio [AP/AR Dashboard Suite](https://github.com/cmrengifor/dashboard-tools-10-ap-and-ar).*
