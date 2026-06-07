# Dashboard 03 — Dispute Resolution Tracker

## Objetivo

Seguimiento del ciclo de vida de disputas de facturas con proveedores: identificar cuellos de botella por tipo de disputa, prioridad y estado, medir tiempo de resolución y tasa de escalamiento para mejorar la gestión de cuentas por pagar.

---

## KPIs

| KPI | Descripción | Fórmula Excel |
|---|---|---|
| **Open Disputes** | Total de disputas activas (Open + In Progress + Escalated) | `=COUNTIF(...,"Open")+COUNTIF(...,"In Progress")+COUNTIF(...,"Escalated")` |
| **Amount in Dispute** | Monto total en disputas activas | `=SUMIF(status,"Open",amount)+SUMIF(status,"In Progress",amount)+SUMIF(status,"Escalated",amount)` |
| **Avg Resolution Days** | Promedio de días para resolver disputas cerradas | `=IFERROR(AVERAGEIF(resolution_days,">0",resolution_days),0)` |
| **Escalation Rate** | % de disputas escaladas sobre el total | `=IFERROR(COUNTIF(status,"Escalated")/COUNTA(dispute_id),0)` |

---

## Dataset

**Archivo:** `data/disputes_data.csv`  
**Filas:** 548 registros  
**Generado con:** `data/generate_data.py`

### Columnas

| Columna | Tipo | Descripción |
|---|---|---|
| dispute_id | String | ID único de disputa (DIS-0001 … DIS-0548) |
| invoice_id | String | Factura asociada a la disputa |
| vendor_id | String | ID del proveedor (VND-001 … VND-020) |
| vendor_name | String | Nombre del proveedor |
| vendor_category | String | IT, Logistics, Materials, Services, Utilities |
| region | String | North, South, East, West, Central |
| dispute_date | Date | Fecha en que se abrió la disputa |
| dispute_type | String | Price Discrepancy / Damaged Goods / Missing Goods / Duplicate Invoice / Service Quality / Contract Terms |
| invoice_amount | Decimal | Monto total de la factura original |
| dispute_amount | Decimal | Monto en disputa |
| priority | String | Low / Medium / High / Critical |
| assigned_to | String | Nombre del responsable de resolución |
| status | String | Open / In Progress / Resolved / Escalated / Closed |
| days_open | Integer | Días desde la fecha de apertura |
| resolution_date | Date | Fecha de resolución (vacío si abierta) |
| resolution_days | Integer | Días hasta resolución (vacío si abierta) |
| resolution_outcome | String | Full Credit / Partial Credit / Payment Adjusted / No Action / Pending |
| credit_amount | Decimal | Monto acreditado de vuelta |

### Distribución de datos

| Status | Registros |
|---|---|
| Resolved | 289 |
| Closed | 101 |
| Escalated | 73 |
| Open | 44 |
| In Progress | 41 |
| **Total** | **548** |

- **Total dispute amount:** $11,898,417
- **Active dispute amount:** $3,431,644
- **Avg resolution days:** 56.8
- **Escalation rate:** 13.3%

---

## Visualizaciones

| Visual | Tipo | Datos |
|---|---|---|
| PT_Type | PivotTable | Dispute Amount por dispute_type |
| PT_Priority | PivotTable | Dispute Amount por priority |
| PT_Status | PivotTable | Dispute Amount por status |
| Chart 1 | Bar Clustered | Dispute Amount by Type |
| Chart 2 | Column Clustered | Dispute Amount by Priority |
| Chart 3 | Doughnut | Disputes by Status |
| TypeSlicer | Slicer | Filtro por dispute_type |
| PrioritySlicer | Slicer | Filtro por priority |
| StatusSlicer | Slicer | Filtro por status |

---

## Estructura del archivo Excel

```
dispute_resolution_tracker.xlsx
├── Dashboard (tab azul)
│   ├── B2      — Título del dashboard (merged B2:P2)
│   ├── B4:N4   — Etiquetas KPI
│   ├── B5:N5   — Valores KPI (con formato de número)
│   ├── B6:N6   — Sub-etiquetas KPI
│   ├── B8:L8   — Encabezados de sección
│   ├── B9      — PivotTable PT_Type (por dispute_type)
│   ├── G9      — PivotTable PT_Priority (por priority)
│   ├── L9      — PivotTable PT_Status (por status)
│   ├── B28:F46 — Chart 1 (Bar — por tipo de disputa)
│   ├── G28:K46 — Chart 2 (Column — por prioridad)
│   ├── L28:P46 — Chart 3 (Doughnut — por estado)
│   ├── B48     — Slicer: dispute_type
│   ├── F48     — Slicer: priority
│   └── J48     — Slicer: status
└── Data (tab gris)
    └── A1:R549 — Tabla Excel "DisputeData" (548 filas + encabezado)
```

---

## Instrucciones de uso

1. Abrir `dispute_resolution_tracker.xlsx` en Microsoft Excel (2016+).
2. La hoja **Dashboard** muestra los KPIs activos y los gráficos de distribución.
3. Usar los **slicers** para filtrar por tipo de disputa, prioridad o estado.
4. Para actualizar datos reales:
   - Reemplazar `data/disputes_data.csv` con exportación del sistema ERP/AP.
   - En la hoja **Data**, mantener el nombre de tabla `DisputeData` y las mismas columnas.
   - Hacer clic derecho en cualquier PivotTable → **Actualizar todo**.

---

*Dashboard generado el 07/06/2026. Parte del portafolio [AP/AR Dashboard Suite](https://github.com/cmrengifor/dashboard-tools-10-ap-and-ar).*
