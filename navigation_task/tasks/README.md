# Tasks Directory - Complete Task Separation

Each task has its own completely isolated structure with task-named files.

## Structure

```
tasks/
├── beach_analysis/                    # Beach video analysis task
│   ├── beach_analysis_questions.json # Task-specific questions
│   ├── videos/                       # Task videos
│   ├── code/
│   │   └── beach_analysis_analysis.py # Task-specific Python script
│   └── results/                      # Auto-generated results
│       ├── beach_analysis_video1_result.json
│       └── beach_analysis_summary.json
└── corridor_navigation/              # Navigation analysis task
    ├── corridor_navigation_questions.json
    ├── videos/
    ├── code/
    │   └── corridor_navigation_analysis.py
    └── results/
```

## How to Use

### 1. Quick Start (Edit bash file parameters)
```bash
# Edit run_pipeline.sh at the top:
TASK_NAME="beach_analysis"        # ← Change this
DESCRIPTION="Your description"    # ← Change this

# Run pipeline
./run_pipeline.sh
```

### 2. Create New Task
```bash
# Edit run_pipeline.sh:
TASK_NAME="my_new_task"

# Run to create structure
./run_pipeline.sh
```

This creates:
- `tasks/my_new_task/my_new_task_questions.json`
- `tasks/my_new_task/code/my_new_task_analysis.py`
- `tasks/my_new_task/videos/`
- `tasks/my_new_task/results/`

### 3. Add Content
- Edit the questions JSON file
- Add videos to the videos/ folder
- Run pipeline again

## Task Naming Convention

All files include the task name for complete separation:
- `{task_name}_questions.json` - Questions configuration
- `{task_name}_analysis.py` - Python analysis script
- `{task_name}_{video_name}_result.json` - Individual results
- `{task_name}_summary.json` - Overall summary

## Example Tasks

**beach_analysis:** Color analysis of beach scenes
- Beach color, dress color, hair color, sky color, woman's position

**corridor_navigation:** Indoor navigation analysis
- Movement direction, environment type, position, speed, landmarks