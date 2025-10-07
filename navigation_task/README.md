# Universal Video QA Pipeline

The simplest possible video analysis system. Just edit 3 lines and run!

## 🚀 Ultra-Simple Usage

1. **Edit parameters in bash file (all at the top):**
   ```bash
   # Edit run_analysis.sh - ALL CUSTOMIZABLE PARAMETERS:

   # Basic Task Setup
   TASK_NAME="beach_analysis"                # ← Your task name
   DESCRIPTION="Beach video color analysis" # ← Description
   VIDEO_FORMATS="*.mp4 *.MP4 *.mov *.MOV" # ← Video types

   # Model & Repo Paths (change if downloaded elsewhere)
   MODEL_PATH="/path/to/your/ST-R1-mcq"     # ← Your model location
   EGO_ST_PATH="/path/to/your/Ego-ST"       # ← Your Ego-ST location
   PYTHON_CMD="python3"                     # ← Your Python command

   # Optional Settings
   CUSTOM_DATASET_PATH=""                   # ← Your dataset path
   FALLBACK_MODEL="Qwen/Qwen2-VL-2B-Instruct" # ← Backup model
   MAX_TIMEOUT="300"                        # ← Timeout per video
   PARALLEL_JOBS="1"                        # ← Number of parallel jobs
   ```

2. **Run (creates structure first time):**
   ```bash
   ./run_analysis.sh
   ```

3. **Edit questions & add videos, then run again:**
   ```bash
   # Edit: tasks/beach_analysis/beach_analysis_questions.json
   # Add videos: tasks/beach_analysis/videos/
   ./run_analysis.sh
   ```

## ✨ Why This is Better

✅ **Universal Pipeline** - One system handles ALL tasks
✅ **3-Line Configuration** - Simplest possible setup
✅ **No Code Duplication** - Single analysis script for everything
✅ **Clean Architecture** - Logic separated by function
✅ **User-Friendly** - Focus on questions, not programming

## 📁 Clean Structure

```
navigation_task/
├── run_analysis.sh ⭐              # 3-line config (ONLY file you edit!)
├── tasks/
│   └── beach_analysis/             # Your task
│       ├── beach_analysis_questions.json  # ← Edit questions
│       ├── videos/                 # ← Add videos
│       └── results/                # Auto-generated results
├── src/
│   ├── universal_analysis.py       # Universal analysis (no editing needed)
│   └── video_qa.py                # Core QA engine
└── utils/
    ├── run_pipeline.py             # Pipeline logic (complex stuff hidden)
    └── pipeline_utils.py           # Helper functions
```

## 🎯 Examples

**Beach Analysis:** Color analysis with 5 questions
**Corridor Navigation:** Movement analysis
**Any Custom Task:** Just change the 3 parameters!

## 🔧 Create Any New Task

1. Edit `TASK_NAME="my_task"` in `run_analysis.sh`
2. Run `./run_analysis.sh` (auto-creates structure)
3. Edit generated questions JSON file
4. Add videos and run again

## ⚙️ Setup

```bash
pip install -r requirements.txt
python models/download_model.py  # One-time setup
```

**Perfect for researchers:** Maximum simplicity, zero coding required!