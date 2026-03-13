# Package A Protocol: Platform Benchmark (RQ1)

## Approval Checkpoint (Must Be Filled Before Running)

- Status: `PENDING`
- Objective: prove measurable setup/runtime advantage and stability behavior of Lucia pipeline.
- Required resources:
  - Lucia setup
  - baseline scripts/workflow
  - weak-network emulation method
  - logging output aligned with `03_session_log_schema.json`
- Estimated effort: 2-3 days with repeats
- Claim impact: supports C1 directly and supports "not only integration" argument.
- Approval record:
  - Approved by:
  - Date:
  - Scope notes:

## Conditions

### Comparison Conditions

1. Baseline workflow (no Lucia unified SDK path)
2. Lucia workflow (session-centered path)

### Runtime Conditions

1. Device mode: USB, Wi-Fi
2. Network condition: normal, weak/lossy
3. Duration: short (1 min), long (30-60 min)

## Tasks

Run each task at least 20 times per condition:

1. Discover and connect device
2. Time-to-first-frame
3. Record 10s clip (time-to-first-recording)
4. Export clip to host

## Metrics

Collect and report:

1. setup success rate
2. p50/p95 per setup step
3. end-to-end latency (mean/p50/p95)
4. fps achieved
5. frame drop rate
6. reconnect count + reconnect p95 time
7. long-run drift/jitter indicators
8. failure-type distribution (taxonomy-aligned)

## Required Outputs

1. Setup friction chart (task time + p95)
2. Runtime stability chart (drop/reconnect over time)
3. Latency distribution plot
4. Table with key condition-wise metrics

## Acceptance Criteria

1. Condition matrix is complete (USB/Wi-Fi x normal/weak x short/long).
2. Each metric is available from logs and independently regenerable.
3. At least one explicit boundary statement is derived from weak-network behavior.

