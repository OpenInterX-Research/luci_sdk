# Ego-ST Video QA Example

Ego-ST style video question-answering system for egocentric navigation videos.

## Files
- `demo_video_qa.py` - Main demonstration script
- `ego_st_question_templates.py` - Question bank with 5 categories
- `video_qa_example.py` - Model inference script (requires ST-R1)
- `ego_st_video_qa_results.json` - Sample results

## Usage
```bash
python demo_video_qa.py
```

## Features
- 39 questions across spatial, temporal, object, spatio-temporal, and navigation categories
- Multiple choice (A-D) and open-ended question formats
- Based on Ego-ST benchmark patterns for egocentric video reasoning

## Video Analyzed
`example.MP4`