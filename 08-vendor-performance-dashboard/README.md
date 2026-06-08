# Dashboard 08 — Vendor Performance Dashboard

## Objetivo

Evaluación integral del desempeño de proveedores para el período enero 2025 – agosto 2026, con 30 proveedores clasificados en 5 categorías. Permite analizar el gasto total por proveedor y categoría, monitorear la calidad del servicio, la tasa de entrega a tiempo y los días promedio de pago, con filtros por año, categoría y estado del proveedor.

---

## KPIs

| KPI | Descripción | Medida DAX |
|---|---|---|
| **Total Spend** | Suma total de todos los montos de factura | `[Total Spend]` |
| **Avg Quality Score** | Promedio del puntaje de calidad (escala 0–100) | `[Avg Quality Score]` |
| **On-Time Delivery %** | Porcentaje de entregas realizadas a tiempo | `[On-Time Delivery %]` |
| **Avg Payment Days** | Promedio de días de pago por factura | `[Avg Payment Days]` |

---

## Dataset

**Archivo:** `data/vendor_performance_data.csv`
**Filas:** 562 registros
**Generado con:** `data/generate_data.py`

### Columnas

| Columna | Tipo | Descripción |
|---|---|---|
| record_id | String | ID único del registro (VP-0001 … VP-0562) |
| vendor_id | String | ID del proveedor (ej. V-LOG-01) |
| vendor_name | String | Nombre del proveedor (ej. "Logistics Vendor 01") |
| category | String | Categoría del proveedor |
| region | String | Región geográfica (North, South, East, West, Central) |
| status | String | Estado: Active, Probation, Inactive |
| period | String | Mes-año (ej. "Jan 2025") |
| year | Integer | Año (2025 o 2026) |
| month | Integer | Número de mes (1–12) |
| quarter | String | Trimestre (Q1–Q4) |
| invoice_amount | Decimal | Monto de factura del período |
| payment_days | Integer | Días de pago registrados |
| on_time | String | Entrega a tiempo: Yes / No |
| quality_score | Decimal | Puntaje de calidad (0–100) |
| defect_rate | Decimal | Tasa de defectos (0.0–1.0) |
| order_count | Integer | Número de órdenes del período |
| dispute_count | Integer | Número de disputas del período |

### Distribución de datos

| category | Proveedores |
|---|---|
| Technology | 6 |
| Office Supplies | 6 |
| Raw Materials | 6 |
| Logistics | 6 |
| Professional Services | 6 |

| status | Distribución |
|---|---|
| Active | ~67% de registros |
| Probation | ~17% de registros |
| Inactive | ~16% de registros |

- **Período:** Enero 2025 – Agosto 2026 (20 meses)
- **Total Spend:** ~$70.9M
- **Avg Quality Score:** ~78.2
- **On-Time Delivery %:** ~88.8%
- **Avg Payment Days:** ~48.9

---

## Medidas DAX

```dax
Total Spend = SUM(vendor_performance_data[invoice_amount])

Avg Quality Score = AVERAGE(vendor_performance_data[quality_score])

On-Time Delivery % = DIVIDE(
    CALCULATE(COUNTROWS(vendor_performance_data), vendor_performance_data[on_time] = "Yes"),
    COUNTROWS(vendor_performance_data),
    0
)

Avg Payment Days = AVERAGE(vendor_performance_data[payment_days])
```

---

## Visualizaciones

| Visual | Tipo | Datos | Posición (X, Y, W, H) |
|---|---|---|---|
| KPI Total Spend | Card (new) | Measure: Total Spend | 20, 20, 260, 120 |
| KPI Avg Quality Score | Card (new) | Measure: Avg Quality Score | 300, 20, 260, 120 |
| KPI On-Time Delivery % | Card (new) | Measure: On-Time Delivery % | 580, 20, 260, 120 |
| KPI Avg Payment Days | Card (new) | Measure: Avg Payment Days | 860, 20, 260, 120 |
| Gasto por Período (línea) | Line Chart | X: period, Y: invoice_amount, Legend: category | 20, 160, 560, 210 |
| Calidad por Categoría (columna) | Clustered Column | X: category, Y: quality_score | 600, 160, 560, 210 |
| Mix por Categoría (dona) | Donut Chart | Legend: category, Values: invoice_amount | 20, 390, 280, 200 |
| Detalle de Proveedores (tabla) | Table | vendor_name, category, Total Spend, Avg Quality Score, On-Time Delivery % | 320, 390, 580, 200 |
| Filtro Año | Slicer | year (range slider) | 20, 610, 370, 80 |
| Filtro Categoría | Slicer | category (list) | 410, 610, 370, 80 |
| Filtro Estado | Slicer | status (list: Active / Probation / Inactive) | 800, 610, 360, 80 |

---

## Instrucciones de uso

1. Abrir `vendor_performance_dashboard.pbix` en **Power BI Desktop** (versión mayo 2024+).
2. La hoja **Page 1** muestra el dashboard completo con 11 visualizaciones.
3. Usar los **slicers** para filtrar:
   - **Año:** deslizar el rango para ver solo 2025 o 2026.
   - **Categoría:** seleccionar una o varias categorías de proveedor.
   - **Estado:** filtrar entre proveedores Active, Probation e Inactive.
4. Para actualizar con datos reales:
   - Reemplazar `data/vendor_performance_data.csv` con exportación del sistema ERP/compras.
   - Mantener los mismos nombres de columna.
   - En Power BI: **Inicio → Actualizar** para refrescar los datos.
   - Ajustar los parámetros en `data/generate_data.py` para regenerar datos simulados con diferente período o número de proveedores.

---

*Dashboard generado el 08/06/2026. Parte del portafolio [AP/AR Dashboard Suite](https://github.com/cmrengifor/dashboard-tools-10-ap-and-ar).*
