# 01 — Invoice Aging Dashboard

**Herramienta:** Power BI  
**Fase:** 1 — Base AP  
**Estado:** 🔄 En progreso

## Objetivo

Visualizar el estado de las facturas emitidas, clasificándolas por antigüedad de vencimiento (aging buckets) para identificar prioridades de cobro y clientes con mayor deuda pendiente.

---

## KPIs del Dashboard

| KPI | Descripción |
|---|---|
| Total Outstanding | Suma de todos los saldos pendientes de cobro |
| Total Invoiced | Suma del monto total facturado |
| % Overdue | Porcentaje del monto vencido sobre el total facturado |
| Avg Days Overdue | Promedio de días de vencimiento en facturas pendientes |
| # Facturas vencidas | Conteo de facturas con status Overdue o Partial |

---

## Dataset

**Archivo:** `data/invoice_aging_data.csv`  
**Filas:** 800  
**Período:** Dic 2024 — Jun 2025

### Columnas

| Columna | Tipo | Descripción |
|---|---|---|
| invoice_id | String | ID único de factura (INV-XXXX) |
| customer_name | String | Nombre del cliente |
| customer_segment | String | Segmento: Corporate / Retail / SMB |
| invoice_date | Date (YYYY-MM-DD) | Fecha de emisión de la factura |
| due_date | Date (YYYY-MM-DD) | Fecha de vencimiento |
| invoice_amount | Decimal | Monto total de la factura (USD) |
| paid_amount | Decimal | Monto pagado hasta la fecha de referencia |
| outstanding_balance | Decimal | Saldo pendiente (invoice_amount - paid_amount) |
| days_overdue | Integer | Días desde el vencimiento (0 si está al día) |
| aging_bucket | String | Current / 1-30 / 31-60 / 61-90 / 90+ |
| status | String | Current / Paid / Partial / Overdue |
| region | String | North / South / East / West / Central |
| sales_rep | String | Representante de ventas responsable |

### Distribución de status en el dataset
| Status | Cantidad |
|---|---|
| Current | 135 |
| Overdue | 279 |
| Partial | 174 |
| Paid | 212 |
| **Total** | **800** |

---

## Medidas DAX

Crear estas medidas en la vista de Datos de Power BI:

```dax
Total Outstanding = SUM(invoice_aging_data[outstanding_balance])

Total Invoiced = SUM(invoice_aging_data[invoice_amount])

% Overdue = DIVIDE([Total Outstanding], [Total Invoiced])

Avg Days Overdue = AVERAGE(invoice_aging_data[days_overdue])

# Facturas Vencidas =
CALCULATE(
    COUNTROWS(invoice_aging_data),
    invoice_aging_data[status] IN {"Overdue", "Partial"}
)
```

---

## Pasos para construir el dashboard en Power BI

1. **Conectar el CSV**
   - Obtener datos → Texto/CSV → seleccionar `data/invoice_aging_data.csv`
   - Verificar que `invoice_date` y `due_date` se detecten como tipo Fecha

2. **Power Query — transformaciones**
   - Cambiar tipo de `invoice_date` y `due_date` a Date
   - Cambiar `invoice_amount`, `paid_amount`, `outstanding_balance` a Decimal Number
   - Cambiar `days_overdue` a Número entero
   - Ordenar `aging_bucket` manualmente: Current → 1-30 → 31-60 → 61-90 → 90+

3. **Crear las medidas DAX** (ver sección anterior)

4. **Visualizaciones**

   | Visual | Tipo | Campos |
   |---|---|---|
   | Total Outstanding | Tarjeta KPI | [Total Outstanding] |
   | % Overdue | Tarjeta KPI | [% Overdue] (formato %) |
   | Avg Days Overdue | Tarjeta KPI | [Avg Days Overdue] |
   | Monto por Aging Bucket | Barra apilada | aging_bucket / outstanding_balance |
   | Top 10 Clientes | Tabla | customer_name, outstanding_balance, days_overdue |
   | Distribución por Segmento | Gráfico de dona | customer_segment / outstanding_balance |
   | Mapa por Región | Barra horizontal | region / outstanding_balance |

5. **Filtros (Slicers)**
   - `region`
   - `customer_segment`
   - `sales_rep`
   - `aging_bucket`
   - `invoice_date` (rango de fechas)

6. **Formato**
   - Paleta: rojo para 90+, naranja para 61-90, amarillo para 31-60, verde para Current
   - Fondo oscuro o claro según preferencia de portafolio

---

## Instrucciones de Uso

1. Abrir `invoice_aging_dashboard.pbix` en Power BI Desktop
2. Si pide actualizar la ruta del origen, apuntar a `data/invoice_aging_data.csv`
3. Usar los slicers de región y sales rep para filtrar por área de negocio
4. El aging bucket "90+" requiere atención inmediata — filtrarlo para reportes de cobranza

---

*Dashboard 01 de 10 — AP/AR Dashboard Suite*
