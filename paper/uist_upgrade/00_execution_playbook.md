# Lucia UIST Full-Paper Execution Playbook

Last updated: 2026-03-11
Target: UIST 2026 technical paper (10-page full first, 5-page fallback if needed)

## Objective

Reframe the current manuscript from "SDK + two case studies" to one system story:

1. A unified session-centered wearable AI prototyping pipeline.
2. Measurable developer-friction reduction.
3. Cross-domain plug-in support with explicit strengths and boundaries.

## Hard Rules (Approval-Gated)

Use these gates exactly:

1. Do not start Package A/B/C data collection until approval is logged.
2. Before each package, present:
   - objective
   - protocol
   - required time/resources
   - expected claim impact
3. Start package execution only after explicit "Approved" from you.
4. If any protocol seems infeasible, stop and confirm with you before changing scope.

## Gate Log

- [ ] Gate A approved (Platform benchmark)
  - Date:
  - Approver:
  - Notes:

- [ ] Gate B approved (Developer productivity pilot)
  - Date:
  - Approver:
  - Notes:

- [ ] Gate C approved (Plug-in ablations)
  - Date:
  - Approver:
  - Notes:

## Work Sequence

### Phase 0: Paper Refactor Using Existing Results (No New Data Yet)

1. Replace abstract and contributions with the 3-claim framing in `01_manuscript_restructure.md`.
2. Reorder manuscript to:
   - Introduction + RQs
   - Related Work
   - System Design (session abstraction + plug-in interface + logs)
   - Evaluation (A/B/C)
   - Discussion, Limitations, Reproducibility
3. Insert claim-evidence matrix from `02_claim_evidence_matrix.md`.
4. Align all reported metrics with the unified session schema in `03_session_log_schema.json`.

### Phase 1: Package A (RQ1, must-do)

Run platform benchmarks after Gate A approval.
Protocol: `04_package_a_platform_benchmark.md`.

### Phase 2: Package B (RQ2, high ROI)

Run internal developer pilot after Gate B approval.
Protocol: `05_package_b_developer_pilot.md`.

### Phase 3: Package C (RQ3, must-do)

Run video-QA + measurement ablations after Gate C approval.
Protocol: `06_package_c_plugin_ablations.md`.

### Phase 4: Analysis and Submission Lock

Use `07_stats_and_reproducibility.md` and `08_submission_checklist.md`.

### Phase 4.5: Pipeline + AI Session Execution (Owner Side)

Use the session runner for analysis/reproducibility tasks owned by pipeline/AI:

1. `s_a_ingest` -> Package A CSV ingest and summary output.
2. `s_b_analyze` -> Package B paired statistics and figure/table outputs.
3. `s_video_qa` -> fixed-path Qwen-first video-QA execution path for task folders under `navigation_task/tasks`.
4. `s_c1_dry` then `s_c1_full` -> video-QA prompt-variant ablation path for the corridor-navigation benchmark.
5. `s_c2_ingest` -> Package C2 measurement CSV ingest and summary output.
6. `s_claim_audit` -> C1/C2/C3 coverage validation before manuscript lock.

Reference:
- workflow: `pipeline_ai/workflows/run_pipeline_ai_sessions.sh`
- manuscript insert text: `09_pipeline_ai_paper_insert.md`

## Minimum Success Condition

The paper is submission-ready when all conditions hold:

1. Each of the 3 contribution claims has:
   - at least one quantitative result,
   - at least one explicit boundary statement.
2. Every figure/table can be regenerated from logs + analysis scripts.
3. Reviewer-risk closure is explicit for:
   - "just integration"
   - "insufficient evidence"
   - "unclear boundaries"
