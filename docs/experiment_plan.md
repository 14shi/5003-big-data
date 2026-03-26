# Experiment and Evaluation Plan

## Objectives
- Validate scalability and responsiveness of the pipeline.
- Compare batch-only vs batch+streaming analytical value.
- Produce report-ready metrics required by course rubric.

## Metrics
1. Batch throughput
   - rows processed per second
   - end-to-end ETL duration
2. Streaming latency
   - event ingestion to BigQuery write delay
   - micro-batch processing time
3. Query performance
   - Tableau query latency from BigQuery
4. Cost efficiency
   - cost per run (Dataproc + VM + BigQuery scan)

## Experiment Matrix
- Data scale: 1x, 3x, 5x sampled dataset size
- Spark resources:
  - single-node Dataproc
  - small multi-node Dataproc
- Stream rate:
  - 5 events/s
  - 20 events/s
  - 50 events/s

## Expected Outputs
- Table: runtime vs data scale
- Table: latency vs event rate
- Figure: cost vs cluster configuration
- Discussion: trade-offs and recommended operating point

## Demo Acceptance Criteria
- Batch tables generated successfully in BigQuery
- Streaming table updates continuously
- Tableau dashboards load all four pages correctly
- At least one optimization insight is documented
