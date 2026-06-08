# Dashboard 06 — Cash Flow Forecasting

## Objetivo

Proyección y seguimiento del flujo de caja de la empresa para el período enero 2025 – diciembre 2026, distinguiendo entre datos reales (Actual: ene 2025 – may 2026) y proyectados (Forecast: jun 2026 – dic 2026). Permite monitorear la liquidez, comparar ingresos vs egresos por categoría y período, y evaluar la cobertura financiera global.

---

## KPIs

| KPI | Descripción | Medida DAX |
|---|---|---|
| **Total Inflows** | Suma total de todos los ingresos (forecast_amount donde flow_type = "Inflow") | `[Total Inflows]` |
| **Total Outflows** | Suma total de todos los egresos (forecast_amount donde flow_type = "Outflow") | `[Total Outflows]` |
| **Net Cash Flow** | Diferencia entre ingresos y egresos totales | `[Net Cash Flow]` |
| **Coverage Ratio** | Ratio de cobertura: Total Inflows / Total Outflows | `[Coverage Ratio]` |

---

## Dataset

**Archivo:** `data/cash_flow_data.csv`
**Filas:** 590 registros
**Generado con:** `data/generate_data.py`

### Columnas

| Columna | Tipo | Descripción |
|---|---|---|
| transaction_id | String | ID único de transacción (CF-0001 … CF-0590) |
| date | Date | Fecha exacta de la transacción |
| period | String | Etiqueta de mes-año (ej. "Jan 2025") |
| year | Integer | Año (2025 o 2026) |
| month | Integer | Número de mes (1–12) |
| quarter | String | Trimestre (Q1–Q4) |
| category | String | AR Collections, Product Sales, Service Revenue, Interest Income, AP Payments, Payroll, Operating Expenses, CAPEX, Tax Payments |
| flow_type | String | Inflow / Outflow |
| department | String | Finance, Operations, HR, Sales, IT |
| region | String | North, South, East, West, Central |
| counterparty | String | Nombre del cliente o proveedor |
| reference | String | Referencia de documento (INV-, ORD-, SVC-, INT-, PO-, PAY-, EXP-, CAP-, TAX-) |
| budget_amount | Decimal | Monto presupuestado |
| actual_amount | Decimal | Monto real (0 para períodos forecast) |
| forecast_amount | Decimal | Monto proyectado (igual al actual en períodos históricos) |
| variance | Decimal | Diferencia actual vs presupuesto (0 para forecast) |
| variance_pct | Decimal | Varianza porcentual (0 para forecast) |
| data_type | String | Actual (ene 2025 – may 2026) / Forecast (jun 2026 – dic 2026) |
| is_favorable | String | Yes / No / (vacío para forecast) |

### Distribución de datos

| flow_type | Registros |
|---|---|
| Inflow | ~280 |
| Outflow | ~310 |

| data_type | Registros |
|---|---|
| Actual | ~420 |
| Forecast | ~170 |

| category | Descripción |
|---|---|
| AR Collections | Cobros de cuentas por cobrar (Inflow) |
| Product Sales | Ventas de productos (Inflow) |
| Service Revenue | Ingresos por servicios (Inflow) |
| Interest Income | Ingresos por intereses (Inflow) |
| AP Payments | Pagos a proveedores (Outflow) |
| Payroll | Nómina bi-semanal (Outflow) |
| Operating Expenses | Gastos operativos varios (Outflow) |
| CAPEX | Inversiones en activos (Outflow) |
| Tax Payments | Pagos de impuestos trimestrales (Outflow) |

- **Total Inflows:** $1.29bn
- **Total Outflows:** $1.15bn
- **Net Cash Flow:** $145M
- **Coverage Ratio:** 1.13

---

## Medidas DAX

```dax
Total Inflows = CALCULATE(SUM(cash_flow_data[forecast_amount]), cash_flow_data[flow_type] = "Inflow")

Total Outflows = CALCULATE(SUM(cash_flow_data[forecast_amount]), cash_flow_data[flow_type] = "Outflow")

Net Cash Flow = [Total Inflows] - [Total Outflows]

Coverage Ratio = DIVIDE([Total Inflows], [Total Outflows], 0)
```

---

## Visualizaciones

| Visual | Tipo | Datos | Posición (X, Y, W, H) |
|---|---|---|---|
| KPI Total Inflows | Card (new) | Measure: Total Inflows | 20, 20, 260, 120 |
| KPI Total Outflows | Card (new) | Measure: Total Outflows | 300, 20, 260, 120 |
| KPI Net Cash Flow | Card (new) | Measure: Net Cash Flow | 580, 20, 260, 120 |
| KPI Coverage Ratio | Card (new) | Measure: Coverage Ratio | 860, 20, 260, 120 |
| Inflows vs Outflows (línea) | Line Chart | X: period, Y: forecast_amount, Legend: flow_type | 20, 160, 560, 210 |
| Forecast by Category (columna) | Clustered Column | X: category, Y: forecast_amount | 600, 160, 560, 210 |
| Inflow vs Outflow Mix (dona) | Donut Chart | Legend: flow_type, Values: forecast_amount | 20, 390, 280, 200 |
| Detalle por Período (tabla) | Table | period, data_type, Total Inflows, Total Outflows, Net Cash Flow | 320, 390, 580, 200 |
| Filtro Año | Slicer | year (range slider) | 20, 610, 370, 80 |
| Filtro Categoría | Slicer | category (list) | 410, 610, 370, 80 |
| Filtro Tipo de Dato | Slicer | data_type (list: Actual / Forecast) | 800, 610, 360, 80 |

---

## Instrucciones de uso

1. Abrir `cash_flow_forecasting.pbix` en **Power BI Desktop** (versión mayo 2024+).
2. La hoja **Page 1** muestra el dashboard completo con 11 visualizaciones.
3. Usar los **slicers** para filtrar:
   - **Año:** deslizar el rango para ver solo 2025 o 2026.
   - **Categoría:** seleccionar una o varias categorías de flujo.
   - **Tipo de dato:** filtrar entre datos Actual (históricos) y Forecast (proyectados).
4. Para actualizar con datos reales:
   - Reemplazar `data/cash_flow_data.csv` con exportación del sistema contable/ERP.
   - Mantener los mismos nombres de columna.
   - En Power BI: **Inicio → Actualizar** para refrescar los datos.
   - Ajustar `ACTUAL_CUTOFF` en `data/generate_data.py` si cambia el corte histórico/forecast.

---

*Dashboard generado el 08/06/2026. Parte del portafolio [AP/AR Dashboard Suite](https://github.com/cmrengifor/dashboard-tools-10-ap-and-ar).*
