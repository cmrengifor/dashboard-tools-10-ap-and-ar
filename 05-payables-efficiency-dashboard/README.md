# Dashboard 05 — Payables Efficiency Dashboard

## Objetivo

Medición de la eficiencia en el proceso de pago de cuentas por pagar: seguimiento del ciclo de pago (DPO), tasa de pago a tiempo, captura de descuentos por pronto pago y saldo pendiente por categoría de proveedor, para optimizar el flujo de caja y las relaciones con proveedores.

---

## KPIs

| KPI | Descripción | Fórmula Excel |
|---|---|---|
| **Total AP Outstanding** | Saldo total pendiente de pago (facturas no pagadas) | `=SUM(PayablesData[outstanding_balance])` |
| **Avg Days to Pay (DPO)** | Promedio de días entre fecha de factura y fecha de pago | `=AVERAGEIF(PayablesData[payment_status],"Paid",PayablesData[days_to_pay])` |
| **On-Time Payment Rate** | % de facturas pagadas en o antes de la fecha de vencimiento | `=IFERROR(COUNTIF(is_on_time,"Yes")/(COUNTIF(status,"Paid")+COUNTIF(status,"Partial")),0)` |
| **Discounts Captured** | Monto total de descuentos por pronto pago capturados | `=SUM(PayablesData[discount_amount])` |

---

## Dataset

**Archivo:** `data/payables_data.csv`
**Filas:** 750 registros
**Generado con:** `data/generate_data.py`

### Columnas

| Columna | Tipo | Descripción |
|---|---|---|
| invoice_id | String | ID único de factura AP (AP-0001 … AP-0750) |
| vendor_id | String | ID del proveedor (VND-001 … VND-025) |
| vendor_name | String | Nombre del proveedor |
| vendor_category | String | Facilities, IT, Logistics, Materials, Services, Utilities |
| region | String | North, South, East, West, Central |
| approver | String | Nombre del aprobador del pago |
| invoice_date | Date | Fecha de recepción de la factura |
| due_date | Date | Fecha de vencimiento (invoice_date + payment_terms) |
| payment_terms | Integer | Días de crédito (15, 30, 45, 60, 90) |
| invoice_amount | Decimal | Monto total de la factura |
| paid_amount | Decimal | Monto pagado |
| outstanding_balance | Decimal | Saldo pendiente (invoice_amount − paid_amount) |
| payment_date | Date | Fecha efectiva de pago (vacío si pendiente) |
| payment_status | String | Paid / Overdue / Partial / Pending |
| payment_method | String | ACH / Wire / Check / Credit Card |
| days_to_pay | Integer | Días desde invoice_date hasta payment_date |
| days_early_late | Integer | días_vencimiento − días_pago (positivo=temprano, negativo=tarde) |
| is_on_time | String | Yes / No / (vacío si no pagada) |
| has_discount_terms | String | Yes / No — si la factura tiene términos de descuento |
| discount_rate | Decimal | Tasa de descuento aplicable (0.005–0.02) |
| discount_captured | String | Yes / No — si se capturó el descuento por pago temprano |
| discount_amount | Decimal | Monto del descuento capturado |

### Distribución de datos

| payment_status | Registros |
|---|---|
| Paid | 546 |
| Overdue | 75 |
| Partial | 72 |
| Pending | 57 |
| **Total** | **750** |

| vendor_category | Registros |
|---|---|
| IT | 168 |
| Logistics | 156 |
| Materials | 151 |
| Utilities | 94 |
| Services | 94 |
| Facilities | 87 |

- **Total AP Outstanding:** $3,775,961
- **Avg Days to Pay:** 43.3 días
- **On-Time Payment Rate:** 53.2%
- **Discounts Captured:** $4,919

---

## Visualizaciones

| Visual | Tipo | Datos |
|---|---|---|
| PT_Category | PivotTable | Outstanding balance por vendor_category |
| PT_Status | PivotTable | Invoice amount por payment_status |
| PT_OnTime | PivotTable | Invoice amount por is_on_time |
| Chart 1 | Bar Clustered | Outstanding by Vendor Category (from PT_Category) |
| Chart 2 | Column Clustered | Invoice Amount by Payment Status (from PT_Status) |
| Chart 3 | Doughnut | On-Time vs Late Payments (from PT_OnTime) |
| CategorySlicer | Slicer | Filtro por vendor_category |
| StatusSlicer | Slicer | Filtro por payment_status |
| RegionSlicer | Slicer | Filtro por region |

---

## Estructura del archivo Excel

```
payables_efficiency_dashboard.xlsx
├── Dashboard (tab azul)
│   ├── B2      — Título del dashboard (merged B2:N2)
│   ├── B4:K4   — Etiquetas KPI (4 KPIs)
│   ├── B5:K5   — Valores KPI (con fórmulas vivas sobre PayablesData)
│   ├── B6:K6   — Sub-etiquetas KPI
│   ├── B8:N8   — Encabezados de sección
│   ├── B9      — PivotTable PT_Category (outstanding por categoría)
│   ├── G9      — PivotTable PT_Status (invoice amount por status)
│   ├── L9      — PivotTable PT_OnTime (invoice amount por on-time)
│   ├── B28:F46 — Chart 1 (Bar — outstanding por categoría)
│   ├── G28:K46 — Chart 2 (Column — invoice amount por status)
│   ├── L28:P46 — Chart 3 (Doughnut — on-time vs late)
│   ├── B48     — Slicer: vendor_category
│   ├── F48     — Slicer: payment_status
│   └── J48     — Slicer: region
└── Data (tab gris)
    └── A1:V751 — Tabla Excel "PayablesData" (750 filas + encabezado)
```

---

## Instrucciones de uso

1. Abrir `payables_efficiency_dashboard.xlsx` en **Microsoft Excel** (2016+).
2. La hoja **Dashboard** muestra los 4 KPIs de eficiencia de pagos y las distribuciones por categoría.
3. Usar los **slicers** para filtrar por categoría de proveedor, estado de pago o región.
4. Para actualizar datos reales:
   - Reemplazar `data/payables_data.csv` con exportación del sistema ERP/AP.
   - Mantener los mismos nombres de columna.
   - En la hoja **Data**, mantener el nombre de tabla `PayablesData`.
   - Hacer clic derecho en cualquier PivotTable → **Actualizar todo**.

---

*Dashboard generado el 07/06/2026. Parte del portafolio [AP/AR Dashboard Suite](https://github.com/cmrengifor/dashboard-tools-10-ap-and-ar).*
