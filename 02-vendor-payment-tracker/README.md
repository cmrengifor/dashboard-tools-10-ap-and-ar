# Dashboard 02 — Vendor Payment Tracker

## Objetivo

Seguimiento de pagos a proveedores: saldos pendientes, facturas vencidas y captura de descuentos por pronto pago. Permite identificar proveedores de alto riesgo y optimizar la gestión de cuentas por pagar.

---

## KPIs

| KPI | Descripción | Fórmula Excel |
|---|---|---|
| **Total Outstanding** | Saldo total pendiente de pago | `=SUM(VendorData[outstanding_balance])` |
| **At-Risk Balance** | Saldo en facturas Overdue + Partial | `=SUMIF(...,"Overdue",...)+SUMIF(...,"Partial",...)` |
| **Avg Payment Days** | Promedio de días pendientes (facturas no pagadas) | `=AVERAGEIF(...,"<>Paid",VendorData[days_outstanding])` |
| **Discount Captured** | Total de descuentos por pronto pago capturados | `=SUM(VendorData[discount_captured])` |

---

## Dataset

**Archivo:** `data/vendor_payment_data.csv`  
**Filas:** 702 registros  
**Generado con:** `data/generate_data.py`

### Columnas

| Columna | Tipo | Descripción |
|---|---|---|
| vendor_id | String | ID único del proveedor (VND-001 … VND-020) |
| vendor_name | String | Nombre del proveedor |
| vendor_category | String | Categoría: IT, Logistics, Materials, Services, Utilities |
| region | String | Región: North, South, East, West, Central |
| invoice_id | String | ID único de factura (INV-0001 … INV-0702) |
| invoice_date | Date | Fecha de emisión de la factura |
| due_date | Date | Fecha de vencimiento |
| payment_terms | Integer | Términos de pago en días (15/30/45/60/90) |
| invoice_amount | Decimal | Monto total de la factura |
| paid_amount | Decimal | Monto pagado hasta la fecha |
| outstanding_balance | Decimal | Saldo pendiente (invoice_amount − paid_amount) |
| payment_date | Date | Fecha de pago efectivo (vacío si no pagado) |
| days_outstanding | Integer | Días desde la fecha de emisión |
| days_overdue | Integer | Días de mora (0 si no vencido) |
| payment_status | String | Paid / Pending / Partial / Overdue |
| discount_rate | Decimal | Tasa de descuento disponible (0%, 1%, 2%, 2.5%) |
| discount_captured | Decimal | Descuento efectivamente capturado |

### Distribución de datos

| Status | Registros |
|---|---|
| Paid | 359 |
| Pending | 187 |
| Partial | 63 |
| Overdue | 93 |
| **Total** | **702** |

- **Total Outstanding:** $11,672,407
- **Discount Captured:** $93,618.96

---

## Visualizaciones

| Visual | Tipo | Datos |
|---|---|---|
| PT_Category | PivotTable | Outstanding por vendor_category |
| PT_Status | PivotTable | Outstanding por payment_status |
| Chart 1 | Column Clustered | Outstanding Balance by Vendor Category |
| Chart 2 | Doughnut | Outstanding by Payment Status |
| CategorySlicer | Slicer | Filtro por vendor_category |
| StatusSlicer | Slicer | Filtro por payment_status |

---

## Estructura del archivo Excel

```
vendor_payment_tracker.xlsx
├── Dashboard (tab azul)
│   ├── B2      — Título del dashboard
│   ├── B4:N4   — Etiquetas KPI
│   ├── B5:N5   — Valores KPI (con formato de número)
│   ├── B6:N6   — Sub-etiquetas KPI
│   ├── B8:N8   — Encabezados de sección
│   ├── B9      — PivotTable PT_Category
│   ├── G9      — PivotTable PT_Status
│   ├── B28:G46 — Chart 1 (Column — por categoría)
│   ├── H28:N46 — Chart 2 (Doughnut — por status)
│   ├── B48     — Slicer: vendor_category
│   └── E48     — Slicer: payment_status
└── Data (tab gris)
    └── A1:Q703 — Tabla Excel "VendorData" (702 filas + encabezado)
```

---

## Instrucciones de uso

1. Abrir `vendor_payment_tracker.xlsx` en Microsoft Excel (2016+).
2. La hoja **Dashboard** se muestra por defecto con los KPIs y gráficos ya calculados.
3. Usar los **slicers** (CategorySlicer, StatusSlicer) para filtrar por categoría de proveedor o estado de pago.
4. Para actualizar datos:
   - Reemplazar `data/vendor_payment_data.csv` con datos reales.
   - En la hoja **Data**, importar el CSV manteniendo el mismo nombre de tabla `VendorData`.
   - Hacer clic derecho en cada PivotTable → **Actualizar** para refrescar todos los cálculos.

---

*Dashboard generado el 07/06/2026. Parte del portafolio [AP/AR Dashboard Suite](https://github.com/cmrengifor/dashboard-tools-10-ap-and-ar).*
