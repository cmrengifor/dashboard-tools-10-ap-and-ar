# Plan de Acción — AP/AR Dashboard Suite

## Contexto del Proyecto

| Campo | Detalle |
|---|---|
| **Objetivo** | Portafolio profesional / CV + implementación en entorno corporativo real |
| **Datos** | Datasets simulados generados para cada dashboard |
| **Nivel técnico** | Power BI y Excel avanzado; DAX básico (SUM, CALCULATE, DIVIDE) |
| **Alcance** | 10 dashboards completos |
| **Timeline** | Sin fecha fija — avance a ritmo propio |
| **Inicio** | Invoice Aging Dashboard |

---

## Estructura del Repositorio

Cada dashboard tiene su propia carpeta con tres componentes:

```
dashboard-tools-10-ap-and-ar/
├── PLAN.md                                    ← este archivo
│
├── 01-invoice-aging-dashboard/
│   ├── data/invoice_aging_data.csv
│   ├── invoice_aging_dashboard.pbix
│   └── README.md
│
├── 02-vendor-payment-tracker/
│   ├── data/vendor_payment_data.csv
│   ├── vendor_payment_tracker.xlsx
│   └── README.md
│
├── 03-dispute-resolution-tracker/
│   ├── data/disputes_data.csv
│   ├── dispute_resolution_tracker.xlsx
│   └── README.md
│
├── 04-receivables-collection-dashboard/
│   ├── data/receivables_data.csv
│   ├── receivables_collection_dashboard.pbix
│   └── README.md
│
├── 05-payables-efficiency-dashboard/
│   ├── data/payables_data.csv
│   ├── payables_efficiency_dashboard.xlsx
│   └── README.md
│
├── 06-cash-flow-forecasting/
│   ├── data/cash_flow_data.csv
│   ├── cash_flow_forecasting.pbix
│   └── README.md
│
├── 07-expense-vs-revenue-dashboard/
│   ├── data/expense_revenue_data.csv
│   ├── expense_vs_revenue_dashboard.pbix
│   └── README.md
│
├── 08-vendor-performance-dashboard/
│   ├── data/vendor_performance_data.csv
│   ├── vendor_performance_dashboard.pbix
│   └── README.md
│
├── 09-customer-credit-risk-dashboard/
│   ├── data/credit_risk_data.csv
│   ├── customer_credit_risk_dashboard.pbix
│   └── README.md
│
└── 10-ap-ar-consolidated-dashboard/
    ├── data/consolidated_data.csv
    ├── ap_ar_consolidated_dashboard.pbix
    └── README.md
```

**Entregables por dashboard:**
- `data/*.csv` — Dataset simulado con datos realistas
- `*.pbix` o `*.xlsx` — Dashboard funcional
- `README.md` — Objetivo, KPIs, columnas del dataset, medidas DAX usadas, instrucciones de uso

---

## Hoja de Ruta

### Fase 1 — Base AP (Facturas y Pagos)
> Foco: Cuentas por pagar y seguimiento de facturas. Excel + Power BI básico.

| # | Dashboard | Herramienta | Estado |
|---|---|---|---|
| 01 | Invoice Aging Dashboard | Power BI | ✅ Completado |
| 02 | Vendor Payment Tracker | Excel | ✅ Completado |
| 03 | Dispute Resolution Tracker | Excel | ✅ Completado |

### Fase 2 — Base AR (Cobros y Clientes)
> Foco: Cuentas por cobrar, eficiencia de cobro y riesgo crediticio.

| # | Dashboard | Herramienta | Estado |
|---|---|---|---|
| 04 | Receivables Collection Dashboard | Power BI | ✅ Completado |
| 05 | Payables Efficiency Dashboard | Excel + Power BI | ✅ Completado |

### Fase 3 — Análisis de Flujo y Proveedores
> Foco: Proyecciones financieras y evaluación de proveedores.

| # | Dashboard | Herramienta | Estado |
|---|---|---|---|
| 06 | Cash Flow Forecasting | Power BI + Excel | ✅ Completado |
| 07 | Expense vs. Revenue Dashboard | Power BI | ✅ Completado |
| 08 | Vendor Performance Dashboard | Power BI | ✅ Completado |

### Fase 4 — Dashboards Ejecutivos
> Foco: Reportes de alto nivel para liderazgo. Mayor complejidad de datos y DAX.

| # | Dashboard | Herramienta | Estado |
|---|---|---|---|
| 09 | Customer Credit Risk Dashboard | Power BI | ⬜ Pendiente |
| 10 | AP/AR Consolidated Dashboard | Power BI | ⬜ Pendiente |

---

## Pasos por Cada Dashboard

Para cada uno de los 10 dashboards, seguir este flujo:

```
1. [ ] Diseñar el dataset simulado (columnas, tipos, volumen ~500-1000 filas)
2. [ ] Generar el CSV con datos realistas
3. [ ] Conectar el CSV en Power BI o Excel
4. [ ] Limpiar y transformar datos con Power Query
5. [ ] Crear medidas DAX básicas si aplica (SUM, CALCULATE, DIVIDE, DATEDIFF)
6. [ ] Construir las visualizaciones clave
7. [ ] Aplicar formato y diseño profesional
8. [ ] Documentar en README.md
9. [ ] Guardar, hacer commit y push al repositorio
```

---

## Dashboard 01 — Invoice Aging Dashboard (PRIMER PASO)

**Herramienta:** Power BI  
**Descripción:** Seguimiento de facturas vencidas, clasificadas por antigüedad y prioridad de cobro.

### KPIs a incluir
- Total facturado vs. total vencido
- Monto por bucket de aging (0-30, 31-60, 61-90, +90 días)
- Top 10 clientes con mayor deuda vencida
- % de facturas vencidas sobre el total
- Días promedio de vencimiento

### Columnas del dataset simulado
| Columna | Tipo | Descripción |
|---|---|---|
| invoice_id | String | ID único de factura |
| customer_name | String | Nombre del cliente |
| customer_segment | String | Segmento (Retail, Corp, SMB) |
| invoice_date | Date | Fecha de emisión |
| due_date | Date | Fecha de vencimiento |
| invoice_amount | Decimal | Monto de la factura |
| paid_amount | Decimal | Monto pagado hasta la fecha |
| outstanding_balance | Decimal | Saldo pendiente |
| days_overdue | Integer | Días de vencimiento (calculado) |
| aging_bucket | String | Categoría: Current / 1-30 / 31-60 / 61-90 / 90+ |
| status | String | Paid / Partial / Overdue / Current |
| region | String | Región geográfica |
| sales_rep | String | Representante de ventas responsable |

### Medidas DAX básicas
```dax
Total Outstanding = SUM(invoices[outstanding_balance])
Total Invoiced = SUM(invoices[invoice_amount])
% Overdue = DIVIDE([Total Outstanding], [Total Invoiced])
Avg Days Overdue = AVERAGE(invoices[days_overdue])
```

### Visualizaciones
- Tarjetas KPI (Total vencido, % overdue, avg days overdue)
- Gráfico de barras apiladas por aging bucket
- Tabla de top clientes con saldo vencido
- Filtros: región, segmento, sales rep, rango de fechas

---

## Convenciones del Proyecto

- **Commits:** Un commit por dashboard completado, con mensaje `feat: complete dashboard-XX - [nombre]`
- **Datasets:** Mínimo 500 filas, máximo 1.000, con variedad realista de valores
- **DAX:** Solo SUM, CALCULATE, DIVIDE, AVERAGEX, DATEDIFF — sin medidas complejas
- **Idioma:** Nombres de columnas en inglés, documentación en español
- **README de cada dashboard:** Seguir la misma estructura (Objetivo → KPIs → Dataset → DAX → Instrucciones)

---

## Seguimiento de Progreso

Actualizar el estado de cada dashboard en la tabla de hoja de ruta:
- ⬜ Pendiente
- 🔄 En progreso
- ✅ Completado

---

*Plan generado el 06/06/2026. Repositorio: [dashboard-tools-10-ap-and-ar](https://github.com/cmrengifor/dashboard-tools-10-ap-and-ar)*
