# Tableau Dashboard Specification

## Data Source
- Connector: Google BigQuery
- Dataset: `mobility_analytics`
- Tables: `mart_trip_hourly`, `mart_zone_daily`, `rt_zone_5m`

## Dashboard 1: Operations Overview
- KPIs:
  - Total trips (selected period)
  - Avg fare
  - Avg trip distance
- Charts:
  - Hourly trip trend (`mart_trip_hourly.hour_bucket` vs `trip_count`)
  - Fare trend (`avg_fare` line)

## Dashboard 2: Spatial Heatmap
- Geographic heatmap by pickup location (`PULocationID`)
- Date filter and weekday/weekend toggle
- Top-N zones table

## Dashboard 3: Weather Impact Analysis
- Scatter: precipitation vs trip_count
- Dual-axis: temperature and trip_count over time
- Insight note section for interpretation

## Dashboard 4: Near-Real-Time Monitoring
- Source: `rt_zone_5m`
- Auto-refresh interval: 1 minute
- Widgets:
  - Latest 5-minute trip count by zone
  - Short-term moving average
  - Alert indicator when trip_count exceeds threshold

## Demo Script (5-7 min)
1. Open overview for business context.
2. Show heatmap to identify hotspot zones.
3. Explain weather-demand relationship.
4. Switch to realtime panel and trigger event producer.
5. Conclude with system benefits over single-machine analytics.
