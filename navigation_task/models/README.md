# Model and Repository Download

## Automatic Download

Download both model and Ego-ST repository:
```bash
python download_model.py
```

## Individual Downloads

Model only:
```bash
python download_model.py --model-only
```

Repository only:
```bash
python download_model.py --repo-only
```

## Manual Download

**ST-R1 Model:**
```bash
hf download openinterx/ST-R1-mcq --local-dir ./ST-R1-mcq
```

**Ego-ST Repository:**
```bash
git clone https://github.com/WPR001/Ego-ST.git
```

## Fallback

The system will use `Qwen/Qwen2-VL-2B-Instruct` if ST-R1 is unavailable.