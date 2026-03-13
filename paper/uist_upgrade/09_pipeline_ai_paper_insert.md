# Pipeline + AI Paper Insert (Ready to Paste)

Last updated: 2026-03-11
Owner scope: Pipeline + AI side only

Use this file as copy-ready manuscript content for the new `pipeline_ai` workflow and sessionized evaluation execution.

---

## 1) System Design Insert (Section 3.x)

### 3.x Session-Oriented Reproducibility Layer

To make the evaluation auditable and regenerable, we implemented a session-oriented reproducibility layer (`pipeline_ai`) on top of Lucia's existing SDK and plug-in structure. The layer standardizes run execution, log serialization, schema validation, statistical analysis, and artifact registration under one command interface.

Each run is represented as a session envelope aligned with a shared logging contract (session ID, task type, timing breakdown, stream/sync state, failure tags, and environment metadata). The current schema now covers `video_qa`, `navigation`, and `measurement` task types so that the same reproducibility layer can capture both the fixed-path Qwen-first video-QA runner and the paper-specific ablation workflows. After each run, the pipeline validates the generated log against the canonical schema and persists artifacts in a fixed layout (`data/raw`, `data/processed`, `figures`, `tables`), enabling deterministic regeneration of manuscript figures and tables.

The same execution entrypoint supports six workflows relevant to this paper: (1) Package A benchmark ingest, (2) Package B paired developer analysis, (3) fixed-path video-QA execution with Qwen as the default preset, (4) Package C1 video-QA prompt-variant ablation execution on the corridor-navigation benchmark, (5) Package C2 measurement ingest, and (6) claim-evidence audit. This design decouples data collection ownership from analysis ownership while preserving one reproducible analysis path.

---

## 2) Evaluation Insert (Section 4.0/4.x)

### 4.x Sessionized Evaluation Workflow (Pipeline + AI Side)

We operationalize evaluation with explicit analysis sessions, each mapped to a claim-supporting output:

1. **Session S-AI-A (Package A ingest):** validate and aggregate platform benchmark CSVs into condition-wise summary tables and latency/stability figures.
2. **Session S-AI-B (Package B analysis):** compute paired within-subject statistics (Wilcoxon signed-rank, paired effect size, confidence intervals) for objective and subjective productivity metrics.
3. **Session S-AI-VQA (Fixed-path video QA):** run the task-folder based video-QA module with `Qwen/Qwen2-VL-2B-Instruct` as the primary preset, persisting per-video result JSONs and validated session logs.
4. **Session S-AI-C1-dry (Video-QA dry-run):** verify the complete C1 execution stack and schema-valid logging without depending on device availability.
5. **Session S-AI-C1 (Video-QA full ablation):** execute C1 prompt-variant ablations (`no_anchor`, `min_anchor`, `structured_anchor`) with stratification tags (route length, scene type, lighting) on the corridor-navigation benchmark.
6. **Session S-AI-C2 (Package C2 ingest):** validate and aggregate measurement ablation outputs from vision/device collection into grouped error/runtime summaries.
7. **Session S-AI-R (Claim audit):** enforce per-claim closure checks (quantitative evidence, figure/table linkage, boundary statement completeness).

This sessionized pipeline was used to ensure each contribution claim is supported by traceable outputs rather than ad hoc post-processing.

---

## 3) Reproducibility Insert (Discussion/Reproducibility Section)

### 5.x Reproducibility Protocol and Regeneration Path

All analysis outputs in this study are generated via command-line workflows that write manifest-linked artifacts. For every produced figure/table, we record source files and generation commands in figure/table manifests. This allows direct replay of the analysis path and reduces manual spreadsheet or plotting drift.

The claim audit stage acts as a pre-submission integrity gate. It programmatically verifies that each claim (C1-C3) includes quantitative evidence, concrete figure/table references, and a non-empty boundary statement. Failed checks halt the workflow and surface missing evidence before manuscript lock.

---

## 4) Workflow Figure Spec (You add the figure)

Use this as the figure structure and caption:

Standalone figure asset:
`paper/uist_upgrade/10_pipeline_workflow_figure.md`

**Figure title:** Sessionized Pipeline + AI Evaluation Workflow  
**Blocks (left to right):**

1. Inputs:
   - Package A CSV (platform benchmark)
   - Package B CSV (developer pilot)
   - fixed task folders (`navigation_task/tasks/<task>/...`) for video QA
   - Package C1 metadata/questions
   - Package C2 CSV (measurement ablation)
2. `pipeline_ai` runner:
   - session creation
   - schema validation
   - fixed-path video-QA execution
   - package-specific analysis
   - manifest registration
   - claim audit
3. Outputs:
   - `data/raw` + `data/processed`
   - task-level result JSON + summary JSON
   - `tables/Tab A1, Tab B1, Tab C1, Tab C2`
   - `figures/Fig A2, Fig B1, Fig C1, Fig C2`
   - `claim_audit_report.csv`

**Suggested caption text:**  
“Pipeline + AI workflow used in our evaluation. Fixed-path video-QA runs and package-specific analysis sessions all write schema-validated logs and manifest-linked outputs, enabling regeneration of manuscript artifacts and pre-submission claim-evidence auditing.”

---

## 5) Runnable Commands for Experimental Results

Use the session runner script:

```bash
bash pipeline_ai/workflows/run_pipeline_ai_sessions.sh <session_name>
```

### Session S-AI-A (Package A ingest)

```bash
export INPUT_CSV=paper/uist_upgrade/templates/package_a_runs.csv
export OUTPUT_ROOT=.
bash pipeline_ai/workflows/run_pipeline_ai_sessions.sh s_a_ingest
```

### Session S-AI-B (Package B analysis)

```bash
export INPUT_CSV=paper/uist_upgrade/templates/package_b_participants.csv
export OUTPUT_ROOT=.
bash pipeline_ai/workflows/run_pipeline_ai_sessions.sh s_b_analyze
```

### Session S-AI-VQA (Fixed-path video QA, Qwen default)

```bash
export TASK_NAME=corridor_navigation
export MODEL_PRESET=qwen
export OUTPUT_ROOT=.
bash pipeline_ai/workflows/run_pipeline_ai_sessions.sh s_video_qa
```

Optional single-video run:

```bash
export TASK_NAME=corridor_navigation
export VIDEO_NAME=hallway_left_turn
export MODEL_PRESET=qwen
bash pipeline_ai/workflows/run_pipeline_ai_sessions.sh s_video_qa
```

### Session S-AI-C1-dry (Video-QA dry-run, no hardware dependency)

```bash
export QUESTIONS_FILE=navigation_task/tasks/corridor_navigation/corridor_navigation_questions.json
export VIDEO_METADATA_CSV=paper/uist_upgrade/templates/package_c_navigation_metadata.csv
export MODEL_PATH=navigation_task/models/ST-R1-mcq
export OUTPUT_ROOT=.
bash pipeline_ai/workflows/run_pipeline_ai_sessions.sh s_c1_dry
```

### Session S-AI-C1 (Video-QA full ablation)

```bash
export QUESTIONS_FILE=navigation_task/tasks/corridor_navigation/corridor_navigation_questions.json
export VIDEO_METADATA_CSV=paper/uist_upgrade/templates/package_c_navigation_metadata.csv
export MODEL_PATH=navigation_task/models/ST-R1-mcq
export FALLBACK_MODEL=Qwen/Qwen2-VL-2B-Instruct
export PROMPT_VARIANTS=no_anchor,min_anchor,structured_anchor
export TIMEOUT=300
export OUTPUT_ROOT=.
bash pipeline_ai/workflows/run_pipeline_ai_sessions.sh s_c1_full
```

Optional manual labels:

```bash
export LABELS_CSV=paper/uist_upgrade/templates/package_c_navigation_labels.csv
```

### Session S-AI-C2 (Package C2 ingest)

```bash
export INPUT_CSV=paper/uist_upgrade/templates/package_c_measurement.csv
export OUTPUT_ROOT=.
bash pipeline_ai/workflows/run_pipeline_ai_sessions.sh s_c2_ingest
```

### Session S-AI-R (Claim audit)

```bash
export COVERAGE_CSV=paper/uist_upgrade/templates/claim_coverage.csv
export CLAIM_MATRIX=paper/uist_upgrade/02_claim_evidence_matrix.md
export OUTPUT_ROOT=.
bash pipeline_ai/workflows/run_pipeline_ai_sessions.sh s_claim_audit
```

---

## 6) Output-to-Paper Mapping

Use these generated files directly in manuscript assembly:

- `navigation_task/tasks/corridor_navigation/results/*_result.json` -> fixed-path video-QA per-video outputs for supplement or qualitative examples
- `navigation_task/tasks/corridor_navigation/results/corridor_navigation_summary.json` -> fixed-path video-QA summary for appendix / reproducibility section
- `tables/a1_platform_metrics.csv` -> Package A summary table (C1 evidence)
- `tables/b1_paired_stats.csv` -> Package B stats table (C2 evidence)
- `tables/c1_navigation_metrics.csv` -> C1 ablation table (C3 video-QA evidence on the corridor-navigation benchmark)
- `tables/c2_measurement_metrics.csv` -> C2 ablation table (C3 measurement evidence)
- `tables/claim_audit_report.csv` -> submission evidence checklist appendix/supplement
- `figures/*.png` -> draft figures (replace with final styled plots if needed)
