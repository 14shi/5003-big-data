# Cost and Risk Checklist (<100 USD)

## Budget Guardrails
- [ ] Use Dataproc only during active execution windows; delete after each session.
- [ ] Prefer single-node for dev/test; switch to small multi-node only for final scalability demo.
- [ ] Limit BigQuery scans using partition filters and selected columns only.
- [ ] Cap streaming demo duration (e.g., 20-30 minutes) to avoid unnecessary VM runtime.
- [ ] Track daily spend in GCP Billing dashboard.

## Estimated Cost Envelope (Course Demo Scale)
- Dataproc (single-node, short runs): ~30-45 USD
- Kafka VM (e2-small, limited hours): ~10-20 USD
- BigQuery storage + query scans: ~5-15 USD
- GCS storage + transfer (small subset): ~5-10 USD
- Buffer: ~10 USD
- Total target: 60-90 USD

## Technical Risks and Mitigations
1. Risk: Kafka setup instability on VM
   - Mitigation: keep single-broker demo topology and include restart script.
2. Risk: Streaming sink latency to BigQuery
   - Mitigation: tune trigger interval and reduce per-batch payload.
3. Risk: Tableau refresh lag
   - Mitigation: use pre-aggregated tables and incremental refresh strategy.
4. Risk: Dataset quality issues (nulls/outliers)
   - Mitigation: add strict schema casting and data quality filters in Spark.
5. Risk: Cloud quota/API limits
   - Mitigation: enable APIs early and run smoke tests before full demo.

## Pre-Demo Go/No-Go Checks
- [ ] Dataproc cluster can run sample Spark job successfully.
- [ ] Kafka topic receives and serves events.
- [ ] BigQuery tables are populated and queryable.
- [ ] Tableau dashboards connect and render all required pages.
- [ ] Teardown script verified to prevent budget overrun.
