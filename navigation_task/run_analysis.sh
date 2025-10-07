#!/bin/bash

# =============================================================================
# VIDEO QA PIPELINE - USER CONFIGURATION
# =============================================================================
# CHANGE THESE PARAMETERS FOR YOUR SETUP:

# Task Configuration
TASK_NAME="beach_analysis"                    # ← Your task name
DESCRIPTION="Beach video analysis"           # ← Task description
VIDEO_FORMATS="*.mp4 *.MP4 *.mov *.MOV"     # ← Video file types

# Model and Repository Paths (change if you downloaded elsewhere)
MODEL_PATH="/{your_path}/luci_navi/ST-R1-mcq"        # ← Path to ST-R1 model
EGO_ST_PATH="/{your_path}/luci_navi/Ego-ST"          # ← Path to Ego-ST repo
PYTHON_CMD="python3"                                        # ← Python command

# Dataset Configuration (for custom datasets)
CUSTOM_DATASET_PATH=""                                       # ← Path to your custom dataset (optional)
FALLBACK_MODEL="Qwen/Qwen2-VL-2B-Instruct"                 # ← Fallback model if ST-R1 not found

# Processing Settings
MAX_TIMEOUT="300"                                            # ← Timeout per video (seconds)
PARALLEL_JOBS="1"                                            # ← Number of parallel processes

# =============================================================================
# DO NOT MODIFY BELOW THIS LINE
# =============================================================================

python3 utils/run_pipeline.py \
  "$TASK_NAME" \
  "$DESCRIPTION" \
  "$VIDEO_FORMATS" \
  "$MODEL_PATH" \
  "$EGO_ST_PATH" \
  "$PYTHON_CMD" \
  "$CUSTOM_DATASET_PATH" \
  "$FALLBACK_MODEL" \
  "$MAX_TIMEOUT" \
  "$PARALLEL_JOBS"