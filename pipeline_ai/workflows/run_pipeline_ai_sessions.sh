#!/usr/bin/env bash
set -euo pipefail

# Pipeline + AI session runner (your side only).
#
# Usage:
#   bash pipeline_ai/workflows/run_pipeline_ai_sessions.sh <session_name>
#
# Sessions:
#   s_a_ingest
#   s_b_analyze
#   s_video_qa
#   s_c1_dry
#   s_c1_full
#   s_c2_ingest
#   s_claim_audit
#
# Common env vars:
#   PYTHON_CMD (default: python3)
#   OUTPUT_ROOT (default: .)
#
# Per-session required env vars are checked at runtime.

SESSION_NAME="${1:-}"
PYTHON_CMD="${PYTHON_CMD:-python3}"
OUTPUT_ROOT="${OUTPUT_ROOT:-.}"

if [[ -z "${SESSION_NAME}" ]]; then
  echo "missing session name"
  exit 2
fi

run_cmd() {
  echo "[RUN] $*"
  "$@"
}

case "${SESSION_NAME}" in
  s_a_ingest)
    : "${INPUT_CSV:?Set INPUT_CSV to package_a_runs.csv}"
    run_cmd "${PYTHON_CMD}" -m pipeline_ai package-a-ingest \
      --input-csv "${INPUT_CSV}" \
      --output-root "${OUTPUT_ROOT}"
    ;;

  s_b_analyze)
    : "${INPUT_CSV:?Set INPUT_CSV to package_b_participants.csv}"
    run_cmd "${PYTHON_CMD}" -m pipeline_ai package-b-analyze \
      --input-csv "${INPUT_CSV}" \
      --output-root "${OUTPUT_ROOT}"
    ;;

  s_video_qa)
    TASK_NAME="${TASK_NAME:-corridor_navigation}"
    MODEL_PRESET="${MODEL_PRESET:-qwen}"
    PYTHON_FOR_CHILD="${PYTHON_FOR_CHILD:-${PYTHON_CMD}}"
    CMD=(
      "${PYTHON_CMD}" -m pipeline_ai video-qa-run
      --task "${TASK_NAME}"
      --model-preset "${MODEL_PRESET}"
      --python-cmd "${PYTHON_FOR_CHILD}"
    )
    if [[ -n "${VIDEO_NAME:-}" ]]; then
      CMD+=(--video "${VIDEO_NAME}")
    fi
    if [[ "${DRY_RUN:-0}" == "1" ]]; then
      CMD+=(--dry-run)
    fi
    run_cmd "${CMD[@]}"
    ;;

  s_c1_dry)
    : "${QUESTIONS_FILE:?Set QUESTIONS_FILE to *_questions.json}"
    : "${VIDEO_METADATA_CSV:?Set VIDEO_METADATA_CSV to package_c_navigation_metadata.csv}"
    : "${MODEL_PATH:?Set MODEL_PATH to ST-R1 model or fallback local path}"
    run_cmd "${PYTHON_CMD}" -m pipeline_ai nav-ablation-run \
      --questions-file "${QUESTIONS_FILE}" \
      --video-metadata-csv "${VIDEO_METADATA_CSV}" \
      --model-path "${MODEL_PATH}" \
      --output-root "${OUTPUT_ROOT}" \
      --dry-run
    ;;

  s_c1_full)
    : "${QUESTIONS_FILE:?Set QUESTIONS_FILE to *_questions.json}"
    : "${VIDEO_METADATA_CSV:?Set VIDEO_METADATA_CSV to package_c_navigation_metadata.csv}"
    : "${MODEL_PATH:?Set MODEL_PATH to ST-R1 model or fallback local path}"
    FALLBACK_MODEL="${FALLBACK_MODEL:-Qwen/Qwen2-VL-2B-Instruct}"
    TIMEOUT="${TIMEOUT:-300}"
    PROMPT_VARIANTS="${PROMPT_VARIANTS:-no_anchor,min_anchor,structured_anchor}"
    PYTHON_FOR_CHILD="${PYTHON_FOR_CHILD:-${PYTHON_CMD}}"
    if [[ -n "${LABELS_CSV:-}" ]]; then
      run_cmd "${PYTHON_CMD}" -m pipeline_ai nav-ablation-run \
        --questions-file "${QUESTIONS_FILE}" \
        --video-metadata-csv "${VIDEO_METADATA_CSV}" \
        --model-path "${MODEL_PATH}" \
        --fallback-model "${FALLBACK_MODEL}" \
        --timeout "${TIMEOUT}" \
        --prompt-variants "${PROMPT_VARIANTS}" \
        --python-cmd "${PYTHON_FOR_CHILD}" \
        --output-root "${OUTPUT_ROOT}" \
        --labels-csv "${LABELS_CSV}"
    else
      run_cmd "${PYTHON_CMD}" -m pipeline_ai nav-ablation-run \
        --questions-file "${QUESTIONS_FILE}" \
        --video-metadata-csv "${VIDEO_METADATA_CSV}" \
        --model-path "${MODEL_PATH}" \
        --fallback-model "${FALLBACK_MODEL}" \
        --timeout "${TIMEOUT}" \
        --prompt-variants "${PROMPT_VARIANTS}" \
        --python-cmd "${PYTHON_FOR_CHILD}" \
        --output-root "${OUTPUT_ROOT}"
    fi
    ;;

  s_c2_ingest)
    : "${INPUT_CSV:?Set INPUT_CSV to package_c_measurement.csv}"
    run_cmd "${PYTHON_CMD}" -m pipeline_ai package-c2-ingest \
      --input-csv "${INPUT_CSV}" \
      --output-root "${OUTPUT_ROOT}"
    ;;

  s_claim_audit)
    : "${COVERAGE_CSV:?Set COVERAGE_CSV to claim_coverage.csv}"
    if [[ -n "${CLAIM_MATRIX:-}" ]]; then
      run_cmd "${PYTHON_CMD}" -m pipeline_ai claim-audit \
        --coverage-csv "${COVERAGE_CSV}" \
        --output-root "${OUTPUT_ROOT}" \
        --claim-matrix "${CLAIM_MATRIX}"
    else
      run_cmd "${PYTHON_CMD}" -m pipeline_ai claim-audit \
        --coverage-csv "${COVERAGE_CSV}" \
        --output-root "${OUTPUT_ROOT}"
    fi
    ;;

  *)
    echo "unknown session: ${SESSION_NAME}"
    echo "allowed: s_a_ingest s_b_analyze s_video_qa s_c1_dry s_c1_full s_c2_ingest s_claim_audit"
    exit 2
    ;;
esac
