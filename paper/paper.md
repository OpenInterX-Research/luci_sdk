# Lucia Paper Blueprint

Last updated: 2026-03-10
Target: UIST-style full paper
Primary goal: turn the current "SDK + two case studies" manuscript into one coherent systems paper centered on a shared session abstraction and plug-in architecture.

## 1. Paper Thesis

The paper should argue one thing clearly:

**Lucia is a session-centered wearable AI prototyping system that reduces engineering friction and supports multiple application classes through a shared execution and logging pipeline.**

This means the paper is not structured as:

- SDK description
- case study 1
- case study 2

It is structured as:

- problem and system thesis
- system architecture
- evidence that the system improves development and supports multiple plug-ins

## 2. Core Claims

Use exactly these three claims throughout the paper:

1. **Unified system claim**
   Lucia provides a session-centered wearable AI prototyping architecture with shared connection, streaming, routing, and logging interfaces.
2. **Developer-efficiency claim**
   Lucia reduces prototyping friction compared with baseline fragmented workflows.
3. **Generality-with-boundaries claim**
   Lucia supports both egocentric video-QA and metric-perception plug-ins, with clear strengths and explicit failure boundaries.

## 3. Best Paper Structure

## Title

Recommended direction:

**Lucia: A Session-Centered Wearable AI Prototyping System for Egocentric Video QA and Metric Perception**

Alternative shorter version:

**Lucia: A Wearable AI Prototyping System with Shared Session Abstractions and Plug-in Modules**

## Abstract

Use the draft in [01_manuscript_restructure.md](/Users/wf24018/home/LUCI/uist_upgrade/01_manuscript_restructure.md), then revise the last two sentences once new experiments are complete.

## 1. Introduction

### Purpose

Establish the research gap, system thesis, and paper contributions.

### Keep from original paper

- The original motivation around the rise of wearable devices and egocentric AI.
- The argument that current software infrastructure for wearable AI remains fragmented.
- The idea that unified SDK support is missing for real-time data acquisition, streaming, and higher-level AI integration.

### Add new content

- Reframe Lucia as a **system contribution**, not just a device SDK.
- Introduce the session abstraction early.
- Add the three claims and RQ1-RQ3 explicitly.
- Add one short paragraph stating that video QA and measurement are representative plug-ins built on the same system interface.

### Section content

Paragraph 1:
- wearable AI is growing
- egocentric data is valuable
- current development workflows are fragmented

Paragraph 2:
- existing work emphasizes devices, models, or applications separately
- what is missing is a reusable prototyping pipeline that connects device access to application execution and reproducible analysis

Paragraph 3:
- introduce Lucia as the proposed answer
- summarize the session-centered architecture in one sentence

Paragraph 4:
- state the three contributions exactly

Paragraph 5:
- introduce RQ1-RQ3
- preview evaluation A/B/C

### Output

- one system figure teaser reference
- contributions list
- research questions

## 2. Related Work

### Purpose

Position Lucia against existing wearable AI systems, egocentric reasoning pipelines, stereo/depth pipelines, and toolkit evaluation papers.

### Keep from original paper

- Original wearable computing background.
- Original egocentric AI and LLM-assisted perception context.
- Original stereo/depth and object measurement references.

### Add new content

- Add a subsection on **toolkits and prototyping infrastructure**.
- Add a subsection on **developer-facing evaluation**.
- Rewrite comparisons so Lucia is compared as a **system layer**, not just an application demo.

### Section content

2.1 Wearable and egocentric AI systems
- smart glasses, wearable cameras, first-person assistants

2.2 Navigation reasoning over egocentric video
- ST-Think style models and video-language reasoning

2.3 Stereo/depth fusion for metric perception
- SGBM, monocular depth, fused pipelines, measurement systems

2.4 Toolkits, SDKs, and developer-facing systems evaluation
- where Lucia is different: shared session object, reproducibility contract, and cross-plug-in execution path

### Output

- one closing paragraph that states the gap:
  existing work rarely evaluates a unified wearable AI prototyping layer with both system and developer evidence.

## 3. System Overview

### Purpose

Make the system design the center of the paper.

### Keep from original paper

- ADB connection workflow
- wireless bridge configuration
- RTSP streaming support
- stereo synchronization support
- device access details that are necessary to explain the pipeline

### Add new content

- Introduce the **session object** as the central abstraction.
- Introduce the **plug-in interface** for downstream applications.
- Introduce the **logging and replay contract**.
- Add failure taxonomy and reproducibility rationale.

### Section content

3.1 Pipeline overview
- User Trigger -> Lucia SDK -> Session Object -> Plug-in Module -> Output -> Logging/Replay

3.2 Device access and transport layer
- USB/ADB support
- wireless bridging
- RTSP streaming
- synchronization pathway

3.3 Session abstraction
- what goes into a session:
  frames/clips, timestamps, device mode, sync metadata, prompt/query, config hash, module version
- why this is the core contribution:
  applications share one input/output/logging contract

3.4 Plug-in interface
- video-QA plug-in (corridor-navigation as one benchmark task)
- measurement plug-in
- future plug-ins can reuse the same envelope

3.5 Logging, replay, and failure taxonomy
- introduce the schema from [03_session_log_schema.json](/Users/wf24018/home/LUCI/uist_upgrade/03_session_log_schema.json)
- explain why reproducibility matters for wearable AI systems papers

### Output

- **Main Figure 1**: full system pipeline
- **Table 1**: session schema summary

## 4. Original Content Mapping

This section should not appear in the final paper. It is for writing preparation only.

### Original material that should be preserved

1. Device/SDK capabilities
- ADB connection
- file access and transfer
- network setup
- wireless bridging
- RTSP streaming

2. Video-QA plug-in material
- ST-Think integration
- route question setup
- retrospective and prospective navigation queries
- metrics such as path correctness, direction-change correctness, and followability
- existing observations about stronger short-range perception vs weaker long-horizon reasoning

3. Measurement plug-in material
- dual-Lucia stereo rig
- monocular and stereo calibration
- SGBM and monocular depth fusion
- LLM-guided object detection/segmentation
- object size estimation
- existing calibration statistics

### Existing results worth preserving

These values were partially recovered from the PDF and should be manually verified against the source manuscript before reuse:

- monocular reprojection error: about `0.210` pixels
- stereo reprojection error: about `0.247` pixels
- epipolar alignment error: about `0.188` pixels
- stereo baseline: about `70.06 mm`
- corridor-navigation video-QA values include stronger short-range perceptual categories and weaker long-horizon reasoning

## 4. Evaluation

This entire section should be the center of the revised paper.

### 4.0 Evaluation Overview

### Purpose

Tell the reader that evaluation is organized by claims, not by demo order.

### Add new content

- One short framing paragraph:
  "We evaluate Lucia through three evidence blocks corresponding to system quality, developer efficiency, and application breadth."

### Output

- roadmap sentence pointing to A/B/C packages

## 4.1 Package A: Platform Benchmark (RQ1)

### Purpose

Show that Lucia improves system-level execution and reliability characteristics.

### Keep from original paper

- Any existing connectivity and streaming implementation detail that explains what is benchmarked

### Add new content

- Baseline comparison
- setup friction tasks
- weak-network and long-run conditions
- p50/p95 reporting

### Section content

4.1.1 Conditions
- baseline workflow vs Lucia workflow
- USB vs Wi-Fi
- normal vs weak/lossy network
- short vs long duration

4.1.2 Tasks and metrics
- discover/connect
- time-to-first-frame
- record clip
- export clip
- latency, fps, drops, reconnects, failures

4.1.3 Results
- report quantitative improvements or tradeoffs
- show where Wi-Fi degrades or reconnect costs rise

4.1.4 Takeaway and boundary
- takeaway sentence tied to Claim 1
- explicit limitation sentence

### Output

- **Figure A1** setup friction comparison
- **Figure A2** runtime stability/latency
- **Table A1** platform metrics summary

## 4.2 Package B: Developer Productivity Pilot (RQ2)

### Purpose

Prove Lucia is useful as a development system, not only a technical integration layer.

### Keep from original paper

- none, this is mostly new

### Add new content

- internal within-subject developer study
- completion time, errors, help requests, LOC/config effort, SUS, NASA-TLX

### Section content

4.2.1 Participants and study design
- 8 internal participants
- within-subject
- counterbalanced order

4.2.2 Tasks
- connect and stream
- record and export
- minimal navigation prototype
- minimal measurement prototype

4.2.3 Measures
- objective
- subjective
- qualitative

4.2.4 Results
- paired plots
- effect sizes
- workload/usability summary

4.2.5 Takeaway and boundary
- Lucia reduces development friction
- limitation: internal pilot and small sample

### Output

- **Figure B1** time/errors/effort summary
- **Table B1** SUS/TLX and paired statistics

## 4.3 Package C: Plug-in Evaluation and Ablations (RQ3)

### Purpose

Show breadth and boundaries using two different application classes on the same session interface.

### Keep from original paper

- all current navigation evaluation content
- all current measurement evaluation content
- all existing plots/tables/results that remain valid

### Add new content

- explicitly rename them as plug-ins
- unify both under one session/logging pipeline
- add ablations and condition stratification

## 4.3.1 Plug-in A: Egocentric Video QA (Corridor-Navigation Benchmark)

### Keep from original paper

- ST-Think integration
- route QA design
- retrospective/prospective tasks
- path correctness, direction-change accuracy, followability
- current qualitative failure observations

### Add new content

- anchor ablation:
  no anchor, minimal anchor, structured anchor
- route complexity stratification
- hallucinated landmark rate
- latency breakdown

### Section content

1. Task and dataset setup
2. Baselines and variants
3. Metrics
4. Quantitative results
5. Failure analysis
6. Takeaway and boundary

### Output

- **Figure C1** video-QA ablation chart
- **Table C1** video-QA metrics by route complexity

## 4.3.2 Plug-in B: Metric Perception and Measurement

### Keep from original paper

- stereo rig design
- calibration procedure
- intrinsic/extrinsic calibration results
- SGBM plus monocular depth fusion
- object size measurement pipeline

### Add new content

- ablation:
  SGBM only, monocular only, fusion
- grouped errors by object type, material, distance, lighting
- failure taxonomy mapping

### Section content

1. Calibration and geometric setup
2. Depth pipeline variants
3. Measurement task definition
4. Quantitative results
5. Condition-wise grouping
6. Takeaway and boundary

### Output

- **Figure C2** depth-fusion ablation
- **Figure C3** grouped size-estimation errors
- **Table C2** calibration and measurement summary

## 5. Discussion

### Purpose

Interpret the results as a systems paper, not as two separate application papers.

### Keep from original paper

- current limitations and future directions

### Add new content

- one subsection on what Lucia enables
- one subsection on explicit system boundaries
- one subsection on reproducibility and why the logging contract matters
- one short subsection titled:
  **Why this is not only integration**

### Section content

5.1 What Lucia contributes beyond application assembly
- the shared session object
- unified routing/logging
- reusable developer workflow

5.2 Boundary conditions
- weak-network instability
- long-horizon navigation failures
- reflective/textureless measurement failures
- limited human-study scale

5.3 Reproducibility
- session logs
- artifacts
- regenerable figures/tables

5.4 Future directions
- more plug-ins
- larger studies
- broader device support

## 6. Conclusion

### Purpose

Close by restating the system contribution and evidence structure.

### Section content

- one sentence on problem
- one sentence on Lucia solution
- one sentence on A/B/C evidence
- one sentence on reproducibility and future use

## 7. Newly Added Content Checklist

These are the major additions that were not part of the original paper and must be written explicitly.

1. New abstract aligned to the system story
2. Exact three-claim contribution framing
3. RQ1-RQ3
4. Session abstraction section
5. Plug-in interface section
6. Unified session logging and replay section
7. Claim-evidence matrix table
8. Package A benchmark section
9. Package B developer pilot section
10. Video-QA anchor ablation subsection
11. Measurement depth-fusion ablation subsection
12. Failure taxonomy subsection
13. "Why this is not only integration" discussion paragraph

## 8. Figures and Tables Plan

Use this target set:

1. Figure 1: end-to-end Lucia pipeline
2. Table 1: session schema summary
3. Figure A1: setup friction comparison
4. Figure A2: runtime latency/stability
5. Table A1: platform benchmark metrics
6. Figure B1: developer study summary
7. Table B1: paired developer-study statistics
8. Figure C1: video-QA ablation
9. Table C1: video-QA metrics and boundary cases
10. Figure C2: depth fusion ablation
11. Figure C3: grouped size-estimation errors
12. Table C2: calibration and measurement summary
13. Table X: claim-evidence matrix
14. Figure X: failure taxonomy with case cards

## 9. Writing Instructions

Use these rules while drafting:

1. Every section must answer: what is the systems contribution here?
2. Every evaluation subsection must end with:
   - one claim-level takeaway
   - one limitation/boundary sentence
3. Keep raw API details minimal in the main paper unless they directly support a claim.
4. Reuse all valid original results, but rewrite their framing so they support the system story.
5. When moving content from the current PDF, mark it during drafting as:
   - `[ORIGINAL]` reused from current manuscript
   - `[NEW]` newly added for the upgraded paper

## 10. Drafting Order

Write in this order:

1. Introduction
2. System Overview
3. Related Work
4. Plug-in A and Plug-in B using existing original results
5. Discussion
6. Then fill in Package A and Package B once new data exists
7. Revise abstract and conclusion last

## 11. Files to Use Alongside This One

Use these together while drafting:

1. [01_manuscript_restructure.md](/Users/wf24018/home/LUCI/uist_upgrade/01_manuscript_restructure.md)
2. [02_claim_evidence_matrix.md](/Users/wf24018/home/LUCI/uist_upgrade/02_claim_evidence_matrix.md)
3. [03_session_log_schema.json](/Users/wf24018/home/LUCI/uist_upgrade/03_session_log_schema.json)
4. [04_package_a_platform_benchmark.md](/Users/wf24018/home/LUCI/uist_upgrade/04_package_a_platform_benchmark.md)
5. [05_package_b_developer_pilot.md](/Users/wf24018/home/LUCI/uist_upgrade/05_package_b_developer_pilot.md)
6. [06_package_c_plugin_ablations.md](/Users/wf24018/home/LUCI/uist_upgrade/06_package_c_plugin_ablations.md)
