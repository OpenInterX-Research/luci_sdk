# AI Environment Setup

This guide sets up the repo's inference-side AI workflow with Anaconda or Miniconda.

Scope:
- `pipeline_ai` orchestration and reproducibility workflows
- `navigation_task` video QA tooling
- local ST-R1 / Qwen2-VL inference for navigation analysis

This guide does not install the heavier ST-R1 training stack under `Ego-ST/ST-R1`.

## 1. Create the Conda environment

Run from the repo root:

```bash
cd /Users/wf24018/home/luci_sdk
conda env create -f environment.ai.yml
conda activate luci-ai
```

## 2. Install PyTorch for your hardware

PyTorch is not pinned in `environment.ai.yml` because the correct command depends on the machine.

### macOS with Anaconda

```bash
conda install -n luci-ai -c pytorch pytorch torchvision -y
```

### NVIDIA CUDA

Use the install command from the PyTorch selector for your exact CUDA version:

<https://pytorch.org/get-started/locally/>

Then verify:

```bash
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
```

### Why the macOS command uses Conda

On macOS, mixing Conda's `llvm-openmp` with pip-installed `torch` can abort on import with:

```text
OMP: Error #15: Initializing libomp.dylib, but found libomp.dylib already initialized.
```

Using the Conda PyTorch build keeps OpenMP on a single runtime and avoids that failure.

## 3. Install the local navigation package

The repo root does not currently have package metadata, so you should run `pipeline_ai` from the repo root.
`navigation_task` does have a `setup.py`, so install that package in editable mode:

```bash
pip install -e ./navigation_task
```

## 4. Verify the environment

Check the core imports and CLI entrypoint:

```bash
python -m pipeline_ai --help
python -c "import torch, transformers, qwen_vl_utils; print('imports ok')"
python -m unittest pipeline_ai.tests.test_session_and_templates pipeline_ai.tests.test_stats_and_audit
```

## 5. Download the model used by navigation inference

For inference-only setup, download just the model:

```bash
python navigation_task/models/download_model.py \
  --model-only \
  --model-path navigation_task/models/ST-R1-mcq
```

If the download is gated or rate-limited, authenticate first:

```bash
huggingface-cli login
```

## 6. Run a dry-run of the AI pipeline

This validates the `pipeline_ai` to `navigation_task` wiring without requiring real video files:

```bash
python -m pipeline_ai nav-ablation-run \
  --questions-file navigation_task/tasks/corridor_navigation/corridor_navigation_questions.json \
  --video-metadata-csv paper/uist_upgrade/templates/package_c_navigation_metadata.csv \
  --model-path navigation_task/models/ST-R1-mcq \
  --output-root . \
  --dry-run
```

## 7. Run a full navigation inference pass

Replace the metadata CSV with one that points to real videos and remove `--dry-run`:

```bash
python -m pipeline_ai nav-ablation-run \
  --questions-file navigation_task/tasks/corridor_navigation/corridor_navigation_questions.json \
  --video-metadata-csv /path/to/nav_metadata.csv \
  --model-path navigation_task/models/ST-R1-mcq \
  --output-root .
```

## Notes

- `pipeline_ai` itself is standard-library-only, but its navigation ablation workflow shells into `navigation_task/src/universal_analysis.py`.
- `navigation_task/src/video_qa.py` selects only `cuda` or `cpu`. In practice, full model inference is CUDA-oriented; CPU is acceptable for import checks and dry-runs but will be slow for real runs.
- If ST-R1 is unavailable, the code falls back to `Qwen/Qwen2-VL-2B-Instruct`.

## Recovery for an Existing Broken macOS Env

If you already installed PyTorch with `pip` and see the duplicate `libomp.dylib` error, replace the pip wheels with the Conda build:

```bash
conda activate luci-ai
pip uninstall -y torch torchvision
conda install -n luci-ai -c pytorch pytorch torchvision -y
python -c "import torch, transformers, qwen_vl_utils; print('imports ok')"
```

Avoid the `KMP_DUPLICATE_LIB_OK=TRUE` workaround unless you only need a one-off diagnostic run.
