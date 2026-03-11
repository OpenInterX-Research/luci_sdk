# Pipeline + AI Runner

This module implements your side of the Lucia workflow:

- fixed-path Qwen/ST-R1 video QA runner
- unified session logs (schema-validated)
- Package A ingest/summaries
- Package B paired analysis
- Package C1 navigation ablation runner
- Package C2 ingest/summaries
- claim coverage audit

## Commands

Run from repo root:

```bash
python3 -m pipeline_ai --help
```

Session wrapper script:

```bash
bash pipeline_ai/workflows/run_pipeline_ai_sessions.sh <session_name>
```

### 1) Fixed-path video QA

This is the main fixed-path runner for the current Ego-ST/Qwen video-QA module.

Inputs are discovered from:

- `navigation_task/tasks/<task>/<task>_questions.json`
- `navigation_task/tasks/<task>/videos/`

Outputs are written to:

- `navigation_task/tasks/<task>/results/`
- `data/raw/package_c/<run_id>/session_log.json`

Run the default corridor-navigation task with Qwen:

```bash
python3 -m pipeline_ai video-qa-run
```

Run one video by name:

```bash
python3 -m pipeline_ai video-qa-run \
  --task corridor_navigation \
  --video hallway_left_turn \
  --model-preset qwen
```

Run the local downloaded ST-R1 model instead:

```bash
python3 -m pipeline_ai video-qa-run \
  --task corridor_navigation \
  --model-preset st-r1
```

Dry-run without real videos or model loading:

```bash
python3 -m pipeline_ai video-qa-run --dry-run
```

Wrapper session:

```bash
TASK_NAME=corridor_navigation MODEL_PRESET=qwen DRY_RUN=1 \
bash pipeline_ai/workflows/run_pipeline_ai_sessions.sh s_video_qa
```

### 2) Package A ingest

```bash
python3 -m pipeline_ai package-a-ingest \
  --input-csv paper/uist_upgrade/templates/package_a_runs.csv \
  --output-root .
```

### 3) Package B analysis

```bash
python3 -m pipeline_ai package-b-analyze \
  --input-csv paper/uist_upgrade/templates/package_b_participants.csv \
  --output-root .
```

### 4) Package C1 navigation ablation (dry-run)

Prepare a metadata CSV with columns:
`video_file,route_length,scene_type,lighting_condition`

Template:
`paper/uist_upgrade/templates/package_c_navigation_metadata.csv`

```bash
python3 -m pipeline_ai nav-ablation-run \
  --questions-file navigation_task/tasks/corridor_navigation/corridor_navigation_questions.json \
  --video-metadata-csv /path/to/nav_metadata.csv \
  --model-path /path/to/ST-R1-mcq \
  --output-root . \
  --dry-run
```

### 5) Package C2 ingest

```bash
python3 -m pipeline_ai package-c2-ingest \
  --input-csv paper/uist_upgrade/templates/package_c_measurement.csv \
  --output-root .
```

### 6) Claim audit

Prepare `claim_coverage.csv` with columns:
`claim_id,quant_metrics_count,figure_ids,boundary_statement,status`

Template:
`paper/uist_upgrade/templates/claim_coverage.csv`

```bash
python3 -m pipeline_ai claim-audit \
  --coverage-csv /path/to/claim_coverage.csv \
  --output-root .
```

## Output layout

Generated artifacts follow:

- `data/raw/package_a|package_b|package_c/...`
- `data/processed/...`
- `figures/...`
- `tables/...`
- `figures/figure_manifest.csv`
- `tables/table_manifest.csv`
