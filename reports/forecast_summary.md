# Network capacity forecast summary

This summary is based on synthetic utilization data only.

- MAE: 4.41
- RMSE: 5.45
- MAPE: 8.31%
- High risk links: 0
- Medium risk links: 1
- Low risk links: 2

## Forecast rows

- wan-01 | metro-core | current=70.2% | forecast=74.3% | risk=medium | monitor
- wan-03 | branch-aggregation | current=60.6% | forecast=63.6% | risk=low | monitor
- wan-02 | enterprise-backup | current=52.0% | forecast=55.8% | risk=low | monitor

## Business impact

- Keep the highest-risk links on the capacity review list first.
- Use the forecast to pre-book maintenance windows before utilization crosses the warning threshold.
- Treat the synthetic data as a planning exercise, not as evidence of production performance.