# Package C Protocol: Plug-in Ablations (RQ3)

## Approval Checkpoint (Must Be Filled Before Running)

- Status: `PENDING`
- Objective: prove one session interface supports egocentric video QA and metric measurement with measurable boundaries.
- Required resources:
  - video-QA benchmark videos/questions
  - measurement benchmark objects/conditions
  - variant controls for anchor and depth-fusion ablations
  - session logs and failure tags
- Estimated effort: 3-4 days
- Claim impact: supports C3 directly and closes breadth/boundary reviewer risk.
- Approval record:
  - Approved by:
  - Date:
  - Scope notes:

## C1: Video-QA Plug-in Ablation (Corridor-Navigation Benchmark)

Primary execution path:

1. fixed-path `video-qa-run` with `Qwen/Qwen2-VL-2B-Instruct` as the default model preset
2. prompt-variant ablation on the same question/video assets through `s_c1_dry` and `s_c1_full`
3. local ST-R1 kept as an alternate preset or matched-run baseline when needed

### Variants

1. no_anchor
2. min_anchor
3. structured_anchor

### Stratification

1. route length: short, medium, long
2. scene type: distinct landmarks vs repetitive corridors
3. condition tags: lighting/motion quality

### Metrics

1. path correctness
2. direction-change correctness
3. followability
4. hallucinated landmark rate
5. answer success rate / valid response rate
6. latency breakdown (capture/prompt/inference/render/end-to-end)
7. failure tag distribution

## C2: Measurement Plug-in Ablation

### Variants

1. SGBM only
2. monocular only
3. fusion (target method)

### Grouping Conditions

1. object type: regular vs irregular
2. material: reflective, textureless, normal
3. distance: near, medium, far
4. lighting: bright, low-light

### Metrics

1. size MAE (mm)
2. relative error (%)
3. detection success rate
4. invalid depth/hole rate
5. runtime
6. failure tag distribution

## Required Outputs

1. video-QA ablation chart by variant and route complexity
2. measurement ablation chart by variant and condition group
3. failure taxonomy distribution with representative case cards

## Acceptance Criteria

1. both plug-ins use the same session/task log envelope.
2. the fixed-path video-QA runner and the C1 ablation path use the same task assets and logged schema.
3. each plug-in has at least one strong result and one clear boundary.
4. ablation conclusions are tied to practical design decisions (not only metric deltas).
