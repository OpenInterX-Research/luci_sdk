# Statistics and Reproducibility Protocol

## Data Layout Convention

Store raw and derived outputs under a stable layout:

1. `data/raw/package_a/`
2. `data/raw/package_b/`
3. `data/raw/package_c/`
4. `data/processed/`
5. `figures/`
6. `tables/`

Use immutable raw files and versioned processed files.

## Statistical Defaults

### Package A and C (benchmark + ablations)

1. report mean, median, p50, p95, and 95% confidence intervals.
2. use condition-wise comparisons with clear sample sizes.
3. do not over-interpret small deltas without interval separation.
4. for C1, distinguish fixed-path video-QA runs from prompt-variant ablation outputs in captions and tables.

### Package B (within-subject pilot)

1. paired nonparametric test for main objective metrics.
2. paired effect size.
3. confidence intervals for key differences.
4. report participant-level paired plots where possible.

## Reproducibility Rules

1. Every manuscript figure/table must map to a script/notebook and input file list.
2. Every metric in paper must be traceable to a field in `03_session_log_schema.json`.
3. Keep one "figure manifest" mapping:
   - figure ID
   - source data file(s)
   - generating command
4. Keep one "table manifest" with the same structure.
5. For the video-QA plug-in, record task folder, model preset (`qwen` or `st-r1`), and result JSON path in the manifest trail.

## Claim Coverage Audit

Before final submission, run this audit:

1. C1 has at least one benchmark figure and one limitation sentence.
2. C2 has paired pilot evidence and one external-validity caveat.
3. C3 has both video-QA and measurement evidence plus failure-boundary text.
