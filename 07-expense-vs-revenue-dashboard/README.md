# Dashboard 07 — Expense vs. Revenue Dashboard

## Objetivo

Comparación integral de ingresos y gastos de la empresa para el período enero 2025 – diciembre 2026, distinguiendo entre datos reales (Actual: ene 2025 – may 2026) y proyectados (Forecast: jun 2026 – dic 2026). Permite analizar la rentabilidad neta por categoría y período, evaluar el margen de ganancia global, y filtrar por año, departamento y tipo de dato.

---

## KPIs

| KPI | Descripción | Medida DAX |
|---|---|---|
| **Total Revenue** | Suma total de todos los ingresos (forecast_amount donde type = "Revenue") | `[Total Revenue]` |
| **Total Expenses** | Suma total de todos los gastos (forecast_amount donde type = "Expense") | `[Total Expenses]` |
| **Net Profit** | Diferencia entre ingresos y gastos totales | `[Net Profit]` |
| **Profit Margin %** | Porcentaje de rentabilidad: Net Profit / Total Revenue | `[Profit Margin %]` |

---

## Dataset

**Archivo:** `data/expense_revenue_data.csv`
**Filas:** 624 registros
**Generado con:** `data/generate_data.py`

### Columnas

| Columna | Tipo | Descripción |
|---|---|---|
| transaction_id | String | ID único de transacción (ER-0001 … ER-0624) |
| date | Date | Fecha exacta de la transacción |
| period | String | Etiqueta de mes-año (ej. "Jan 2025") |
| year | Integer | Año (2025 o 2026) |
| month | Integer | Número de mes (1–12) |
| quarter | String | Trimestre (Q1–Q4) |
| type | String | Revenue / Expense |
| category | String | Categoría del ingreso o gasto |
| department | String | Finance, Operations, HR, Sales, IT, Marketing, R&D |
| region | String | North, South, East, West, Central |
| budget_amount | Decimal | Monto presupuestado |
| actual_amount | Decimal | Monto real (0 para períodos forecast) |
| forecast_amount | Decimal | Monto proyectado (igual al actual en períodos históricos) |
| variance | Decimal | Diferencia actual vs presupuesto (0 para forecast) |
| variance_pct | Decimal | Varianza porcentual (0 para forecast) |
| data_type | String | Actual (ene 2025 – may 2026) / Forecast (jun 2026 – dic 2026) |
| is_favorable | String | Yes / No / (vacío para forecast) |

### Distribución de datos

| type | Registros |
|---|---|
| Revenue | ~312 |
| Expense | ~312 |

| data_type | Registros |
|---|---|
| Actual | ~442 |
| Forecast | ~182 |

### Categorías de Revenue
| Categoría | Descripción |
|---|---|
| Product Sales | Ventas de productos |
| Service Revenue | Ingresos por servicios |
| Subscription Revenue | Ingresos por suscripciones |
| Consulting Revenue | Ingresos por consultoría |
| Other Revenue | Otros ingresos |

### Categorías de Expense
| Categoría | Descripción |
|---|---|
| Cost of Goods Sold | Costo de bienes vendidos |
| Salaries & Benefits | Sueldos y beneficios |
| Marketing & Advertising | Marketing y publicidad |
| Operations & Facilities | Operaciones e instalaciones |
| Technology & IT | Tecnología e IT |
| Research & Development | Investigación y desarrollo |
| General & Administrative | Gastos generales y administrativos |
| Depreciation | Depreciación |

- **Total Revenue:** ~$1.18bn
- **Total Expenses:** ~$956M
- **Net Profit:** ~$221M
- **Profit Margin %:** ~19%

---

## Medidas DAX

```dax
Total Revenue = CALCULATE(SUM(expense_revenue_data[forecast_amount]), expense_revenue_data[type] = "Revenue")

Total Expenses = CALCULATE(SUM(expense_revenue_data[forecast_amount]), expense_revenue_data[type] = "Expense")

Net Profit = [Total Revenue] - [Total Expenses]

Profit Margin % = DIVIDE([Net Profit], [Total Revenue], 0)
```

---

## Visualizaciones

| Visual | Tipo | Datos | Posición (X, Y, W, H) |
|---|---|---|---|
| KPI Total Revenue | Card (new) | Measure: Total Revenue | 20, 20, 260, 120 |
| KPI Total Expenses | Card (new) | Measure: Total Expenses | 300, 20, 260, 120 |
| KPI Net Profit | Card (new) | Measure: Net Profit | 580, 20, 260, 120 |
| KPI Profit Margin % | Card (new) | Measure: Profit Margin % | 860, 20, 260, 120 |
| Revenue vs Expenses (línea) | Line Chart | X: period, Y: forecast_amount, Legend: type | 20, 160, 560, 210 |
| Forecast por Categoría (columna) | Clustered Column | X: category, Y: forecast_amount | 600, 160, 560, 210 |
| Mix Revenue vs Expense (dona) | Donut Chart | Legend: type, Values: forecast_amount | 20, 390, 280, 200 |
| Detalle por Período (tabla) | Table | period, data_type, Total Revenue, Total Expenses, Net Profit | 320, 390, 580, 200 |
| Filtro Año | Slicer | year (range slider) | 20, 610, 370, 80 |
| Filtro Departamento | Slicer | department (list) | 410, 610, 370, 80 |
| Filtro Tipo de Dato | Slicer | data_type (list: Actual / Forecast) | 800, 610, 360, 80 |

---

## Instrucciones de uso

1. Abrir `expense_vs_revenue_dashboard.pbix` en **Power BI Desktop** (versión mayo 2024+).
2. La hoja **Page 1** muestra el dashboard completo con 11 visualizaciones.
3. Usar los **slicers** para filtrar:
   - **Año:** deslizar el rango para ver solo 2025 o 2026.
   - **Departamento:** seleccionar uno o varios departamentos.
   - **Tipo de dato:** filtrar entre datos Actual (históricos) y Forecast (proyectados).
4. Para actualizar con datos reales:
   - Reemplazar `data/expense_revenue_data.csv` con exportación del sistema contable/ERP.
   - Mantener los mismos nombres de columna.
   - En Power BI: **Inicio → Actualizar** para refrescar los datos.
   - Ajustar `ACTUAL_CUTOFF` en `data/generate_data.py` si cambia el corte histórico/forecast.

---

*Dashboard generado el 08/06/2026. Parte del portafolio [AP/AR Dashboard Suite](https://github.com/cmrengifor/dashboard-tools-10-ap-and-ar).*
