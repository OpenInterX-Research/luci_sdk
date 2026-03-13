# Lucia → UIST-Style Experimental Research Guide (Copy/Paste)

## Implementation Pack (Generated 2026-03-10)

This guide now has an executable companion pack in `uist_upgrade/`:

1. `uist_upgrade/00_execution_playbook.md` (master workflow + approval gates)
2. `uist_upgrade/01_manuscript_restructure.md` (new abstract/contributions/section map)
3. `uist_upgrade/02_claim_evidence_matrix.md` (required claim-to-evidence table)
4. `uist_upgrade/03_session_log_schema.json` (public logging contract)
5. `uist_upgrade/04_package_a_platform_benchmark.md` (RQ1 protocol)
6. `uist_upgrade/05_package_b_developer_pilot.md` (RQ2 protocol)
7. `uist_upgrade/06_package_c_plugin_ablations.md` (RQ3 protocol)
8. `uist_upgrade/07_stats_and_reproducibility.md` (analysis/repro rules)
9. `uist_upgrade/08_submission_checklist.md` (deadline and readiness lock)

Approval rule enforced in the pack:

- Package A/B/C are marked `PENDING`.
- Do not execute any package until explicit approval is logged in `00_execution_playbook.md`.

This document is a **research + experiment guide** to transform the current “SDK + two case studies” work into a more **UIST-aligned** system paper story:
> **A unified wearable AI prototyping pipeline** based on a **session abstraction** + **plug-in modules**, supported by strong **system + developer + application** evidence.

---

## 1) Current → Target framing (what we are changing)

### Current (risk)
- Reads like: **Platform/SDK introduction** + **Case 1 (navigation)** + **Case 2 (stereo measurement)**.
- Reviewer risk: “Is this *just integration* of existing components/models?” “Where is the core *research contribution*?” “Where is evidence matching claims?”

### Target (UIST-style)
- Reads like: **Unified interactive pipeline** (user intent → SDK session → plug-in modules → output + logging)  
- With a clear thesis:
  - **Lucia SDK reduces friction** for wearable egocentric AI prototyping (connect/stream/sync/log/replay)
  - **Lucia improves developer productivity** (time-to-prototype, LOC, errors, usability)
  - **Lucia supports diverse application classes** (temporal reasoning vs metric perception)
  - *(Optional)* End-user interaction loop is usable and understandable

---

## 2) Unified system pipeline (single “main figure” concept)

### Core loop
**User Trigger → Lucia SDK → Session Object → Plug-in Module → Output Rendering → Logging/Replay**

### Step-by-step example pipeline
1) **Trigger** (voice / phone UI / button / script)
2) **SDK Connection** (USB / Wi-Fi bridge)
3) **Stream** (RTSP ingestion, buffering)
4) **Session Construction**  
   A standard internal object representing everything needed for downstream modules:
   - frames/clips, timestamps, device mode, sync metadata, prompt/query, config hash
5) **Routing to plug-in**
   - **Navigation plug-in** (temporal reasoning / route QA)
   - **Measurement plug-in** (stereo depth + segmentation + size)
6) **Output**
   - text + optional voice + phone UI + confidence + action steps
7) **Logging**
   - latency breakdown, stability stats, failures, artifacts for replay & debugging

**Key principle:** Navigation and Measurement are **not separate “contributions”**; they are **two plug-ins** built on the same session abstraction.

---

## 3) Claims → Research Questions (RQ) (what experiments must prove)

### RQ1 (System / SDK)
**Does Lucia measurably improve connectivity/streaming/synchronization stability and speed?**

### RQ2 (Developer productivity)
**Does Lucia reduce prototyping cost (time, code, errors, learning burden) compared to baseline workflows?**

### RQ3 (Application breadth)
**Can the same session abstraction support both (a) temporal reasoning navigation and (b) metric perception measurement, with clear strengths/limits?**

### RQ4 (Interaction loop, optional but strong)
**Is the end-to-end user interaction loop usable, understandable, and executable?**

---

## 4) Unified session logging schema (foundation for all experiments)

### Why this matters
- Enables consistent benchmarking across all experiments
- Supports failure taxonomy + reproducibility + ablation studies

### Minimal session log fields (suggested)
```json
{
  "session_id": "uuid",
  "timestamp": "ISO8601",
  "device_mode": "USB|WIFI",
  "device_count": 1,
  "stream": {
    "resolution": "WxH",
    "fps_target": 30,
    "latency_ms": {"mean": 0, "p50": 0, "p95": 0},
    "frame_drop_rate": 0.0,
    "reconnect_count": 0,
    "reconnect_time_ms_p95": 0
  },
  "sync": {
    "enabled": false,
    "delta_t_ms": {"mean": 0, "p95": 0},
    "sync_fail_rate": 0.0
  },
  "artifacts": {
    "frame_paths": [],
    "clip_path": "",
    "stereo_pair_paths": []
  },
  "task": {
    "type": "navigation|measurement",
    "query_text": "",
    "prompt_variant": "no_anchor|min_anchor|structured_anchor",
    "module_version": "hash"
  },
  "timing_ms": {
    "capture": 0,
    "prompt_build": 0,
    "inference": 0,
    "postprocess": 0,
    "render": 0,
    "end_to_end": 0
  },
  "result": {
    "success": true,
    "output_text": "",
    "confidence": 0.0,
    "metrics": {}
  },
  "failure": {
    "failed": false,
    "type": "none|connect|stream|sync|nav|measure|mask|depth|other",
    "note": ""
  },
  "env": {
    "network_condition": "normal|weak|lossy",
    "runtime": "pc_specs_hash"
  }
}
````

---

## 5) Experiment plan overview (A–D)

### Package A — Platform/SDK Benchmark (RQ1) **(must-do)**

Goal: Prove measurable SDK advantages in **speed, stability, sync**.

### Package B — Developer Productivity Study (RQ2) **(highest ROI)**

Goal: Prove Lucia reduces **time-to-prototype**, **LOC**, **errors**, and improves usability.

### Package C — Plug-in / Application Evaluation (RQ3)

Goal: Keep navigation + measurement, but position them as **two plug-ins**. Add ablations & boundary analyses.

### Package D — End-user Interaction Pilot (RQ4) **(optional but adds UIST flavor)**

Goal: Show real tasks are understandable/executable with minimal friction.

### Failure taxonomy (cross-cutting, must collect throughout)

Goal: Convert limitations into a structured and publishable insight.

---

## 6) Package A: Platform / SDK Benchmark (RQ1)

### A0: Baselines (comparison conditions)

* **Baseline (no SDK):** ADB + FFmpeg/RTSP + scattered scripts
* **Ours:** Lucia SDK unified interface + session logging
  *(Optional baseline if available: official/vendor workflow)*

### A1: Setup friction benchmark

**Tasks (repeat each N times, e.g., N=20):**

1. discover device → connect success
2. time-to-first-frame
3. start 10s recording → time-to-first-recording
4. export clip to host

**Metrics:**

* success rate
* p50/p95 times for each step
* steps/commands count (effort proxy)
* failure types distribution (permission, stream init, device mismatch)

### A2: RTSP stream stability benchmark

**Variables:**

* USB vs Wi-Fi
* normal vs weak network (bandwidth limit / packet loss / jitter)
* run duration: 1 min vs 30–60 min

**Metrics:**

* end-to-end latency (mean/p50/p95)
* FPS achieved
* frame drop rate
* stutter count (freeze events)
* reconnect count + reconnect p95 time
* long-run drift (timestamp jitter)

### A3: Dual-device synchronization benchmark (if stereo)

**Task:**

* collect synced stereo pairs at a fixed rate (e.g., 1–5 pairs/sec) over 10–15 min

**Metrics:**

* Δt distribution (mean/p95)
* sync failure rate
* correlation: Δt vs depth error (later used in measurement evaluation)

**Deliverables (figures/tables):**

* setup times bar chart + p95
* latency distributions
* stability line plots (drop rate over time)
* sync error histogram

---

## 7) Package B: Developer Productivity Study (RQ2)

### Why it’s critical

This is the strongest evidence that “SDK = research contribution,” not just engineering.

### B1: Participants

* 6–12 participants with basic Python familiarity (lab mates ok)
* within-subject design recommended (each participant does both conditions)

### B2: Conditions

* **Without Lucia SDK:** given baseline instructions for raw workflows
* **With Lucia SDK:** given Lucia docs + API examples

Counterbalance order to reduce learning effects.

### B3: Tasks (4 tasks recommended)

1. Connect + view live stream + save a screenshot
2. Record & export a 10s clip
3. Build a minimal navigation QA prototype (query → answer)
4. Build a minimal measurement prototype (object → size result)

### B4: Metrics

**Objective**

* completion time per task
* success rate
* error count (exceptions, wrong commands)
* “stuck” count / help requests
* LOC (or config lines) needed

**Subjective**

* NASA-TLX (workload)
* SUS (usability)
* quick Likert: “I can extend this to a new app easily”

**Qualitative**

* 5-min interview: top 2 helpful parts + top 2 pain points

### Deliverables

* time-to-prototype box plots
* LOC comparison
* SUS/TLX summary
* qualitative themes → design lessons section

---

## 8) Package C: Plug-in / Application Evaluation (RQ3)

### Core idea

Navigation and Measurement remain, but are reframed as:

* **Plug-in A: Temporal reasoning / navigation guidance**
* **Plug-in B: Metric perception / object measurement**
  Both consume the **same session abstraction** and produce results through the same output/logging channel.

---

### C1: Navigation plug-in evaluation

#### C1.1 Core metrics (keep + strengthen)

* path correctness / step correctness
* direction-change correctness
* followability (human or structured evaluation)
* hallucinated landmark rate (very important)

#### C1.2 End-to-end latency breakdown (system-style)

Measure and report:

* capture time
* prompt building time
* inference time
* rendering time
* end-to-end time

Deliver: breakdown bar chart.

#### C1.3 Anchor/prompt ablation (prove “SDK middle layer” value)

Compare:

* **No anchors** (query only)
* **Minimal anchors** (simple landmark list)
* **Structured anchors** (room tags, keyframes, or simple topology summary)

Report improvements in:

* correctness/followability
* hallucination rate
* latency overhead

#### C1.4 Complexity stratification + boundary conditions

Split results by:

* route length: short/medium/long
* environment similarity: repetitive corridors vs distinct areas
* lighting change / motion blur level
* clip length / rolling window mode (if supported)

Deliver: stratified performance + failure cases.

---

### C2: Measurement plug-in evaluation (stereo + size)

#### C2.1 Geometry confidence (calibration quality)

Report:

* reprojection error (mono & stereo)
* epipolar consistency / stereo RMS error
* stability across time (repeat calibration or check drift)

#### C2.2 Depth fusion ablation (avoid “model stacking” critique)

Compare:

* **SGBM only** (metric but sparse/noisy)
* **Monocular depth only** (dense but scale-ambiguous)
* **Fusion** (your alignment approach)

Metrics:

* depth MAE or relative error (use small GT set if needed)
* hole rate / invalid depth percentage
* edge stability / consistency
* runtime

#### C2.3 Size estimation task (final utility)

Evaluate across conditions:

* object type: regular vs irregular
* material: reflective / textureless / normal
* distance: near/medium/far
* lighting: bright/low light

Metrics:

* size MAE (mm) and relative error (%)
* detection success rate
* failure type distribution (mask failure vs depth failure vs sync issue)

Deliver: grouped error bars + representative successes/failures.

---

## 9) Package D: End-user Interaction Pilot (RQ4) *(Optional but recommended)*

### Goal

Demonstrate the system is not just a backend pipeline—users can execute tasks with it.

### Setup

* 6–8 participants
* two tasks:

  1. “How do I get back to X?” (navigation)
  2. “What is this and how big is it?” (measurement)

### Metrics

* task success rate
* completion time
* user-rated understandability
* trust/confidence rating
* preference: voice vs phone vs button

Deliver: small table + a few representative quotes.

---

## 10) Failure taxonomy (must-do across A–D)

### Why

Failure analysis turns “limitations” into “research contribution” and helps reviewers trust your system.

### Failure tags (suggested)

**Platform**

* connect_fail
* stream_init_fail
* frame_drop_high
* reconnect_slow
* sync_drift

**Navigation**

* long_horizon_error
* landmark_hallucination
* repetitive_corridor_confusion
* instruction_not_actionable

**Measurement**

* reflective_surface_fail
* textureless_fail
* mask_error
* depth_hole
* scale_alignment_fail

### Deliverables

* failure distribution chart
* 3–6 “case cards” with images + short explanation + potential fix

---

## 11) Minimal viable plan: short paper vs standard paper

### If targeting **Short Paper (5 pages)**

Do:

* Package A (core system benchmark)
* Package B (developer study)
* Package C (2 plug-ins, lighter but with 1 key ablation each)
* Failure taxonomy summary

### If targeting **Standard Paper (10 pages)**

Do all above +:

* deeper ablations & stratification
* Package D pilot
* richer design lessons + reproducibility artifacts

---

## 12) Recommended timeline (example 3-week sprint)

### Week 1 — System consolidation

* finalize session schema + logging
* unify pipeline diagram
* implement consistent benchmarks harness
* prepare baseline scripts (no SDK)

### Week 2 — Evidence core

* run Package A (repeatable, multiple conditions)
* run Package B (developer study)
* initial analysis + plots

### Week 3 — Application strengthening

* run C1 anchor ablation + complexity stratification
* run C2 fusion ablation + condition grouping
* collect failure taxonomy examples
* optional D pilot

---

## 13) Final deliverable checklist (figures/tables to plan for)

1. Setup friction comparison (time-to-first-frame/recording, p95)
2. Stream latency & stability curves (drop rate, reconnect p95)
3. Dual-pin sync error distribution (+ correlation to depth error)
4. Developer study: time, LOC, SUS, TLX
5. Navigation results (core metrics) + end-to-end breakdown
6. Navigation ablation (anchors)
7. Stereo calibration quality summary table
8. Depth ablation (SGBM vs mono vs fusion)
9. Size estimation errors grouped by conditions
10. Failure taxonomy + case cards

---

## 14) “Do / Don’t” guidance (to stay UIST-aligned)

### Do

* make **SDK/session abstraction** the central contribution
* match each claim with a measurable experiment
* emphasize reproducibility via logs + artifacts
* present navigation/measurement as plug-ins proving breadth

### Don’t

* rely only on “model accuracy improvements” without system-level evidence
* let two case studies look like separate projects
* skip developer evidence (it’s the strongest support for toolkit papers)

---

## 15) Quick templates (optional)

### Developer study instruction sheet (1 paragraph)

* Provide participants with task descriptions, allowed resources, and success criteria.
* Log time, errors, help requests, and collect SUS/TLX after tasks.

### Weak-network test recipe (simple)

* Limit bandwidth or introduce packet loss using standard tools.
* Keep conditions consistent and document parameters in session logs.

---

## 16) One-sentence new “evaluation story”

We evaluate Lucia as a wearable AI prototyping system through **(A) platform benchmarks** (speed/stability/sync), **(B) developer productivity studies** (time-to-prototype/LOC/usability), and **(C) two representative plug-ins** (temporal navigation + metric measurement) with **ablations and failure taxonomy** to establish generality and practical boundaries.
