# Manuscript Restructure and Text Blocks

## A. New Abstract Draft (Replace Current Abstract)

Wearable AI research is often slowed by fragmented pipelines that couple device access, streaming, and model integration in ad hoc ways. We present Lucia, a session-centered wearable AI prototyping system that unifies device connection, real-time stream ingestion, task routing, and reproducible logging through a single SDK workflow. The core design is a shared session abstraction and plug-in interface that allow heterogeneous applications to run on the same execution and logging backbone. We evaluate Lucia with three evidence blocks: (1) platform benchmarks for setup friction and runtime stability across USB/Wi-Fi and network conditions, (2) an internal developer productivity pilot comparing Lucia against baseline workflows, and (3) plug-in evaluations on two representative application classes: egocentric video question answering and metric measurement. Results position Lucia as a systems contribution that reduces prototyping friction while preserving application breadth, and they expose clear boundary conditions through a structured failure taxonomy. Lucia is released with reproducible logging conventions to support future wearable AI research.

## B. Contribution Statements (Use Exactly 3)

Use this list in the introduction and conclusion:

1. **Unified system contribution:** a session-centered wearable AI prototyping architecture with a shared plug-in interface and reproducible logging contract.
2. **Developer efficiency contribution:** empirical evidence that the Lucia workflow reduces prototyping friction versus baseline scripting workflows.
3. **Generality-with-boundaries contribution:** evidence that one session interface supports both egocentric video-QA and metric-perception plug-ins, with explicit limitations and failure modes.

## C. Research Questions (RQs)

Insert these RQs at the end of introduction:

- **RQ1 (System):** Does Lucia improve setup/runtime reliability and latency characteristics versus baseline workflows?
- **RQ2 (Developer):** Does Lucia reduce prototyping cost (time, errors, implementation effort, subjective workload)?
- **RQ3 (Application breadth):** Can one session abstraction support both egocentric video QA and metric measurement with meaningful performance and clear boundaries?

## D. 10-Page Section Architecture

Use this order:

1. **Introduction (1.0-1.25 pages)**
   - problem: fragmented wearable AI workflows
   - system thesis (Lucia as pipeline)
   - 3 contributions
   - RQ1-RQ3
2. **Related Work (0.75-1.0 page)**
   - wearable AI tooling/platforms
   - egocentric video-QA and route-reasoning systems
   - stereo/depth fusion pipelines
   - developer-toolkit evaluations in HCI/systems
3. **System Design (1.5-2.0 pages)**
   - main figure: Trigger -> Lucia SDK -> Session -> Plug-in -> Output -> Logging
   - session abstraction and plug-in interface
   - logging schema and failure taxonomy
4. **Evaluation (4.0-4.5 pages)**
   - Package A: platform benchmark (RQ1)
   - Package B: developer pilot (RQ2)
   - Package C: plug-in ablations (RQ3)
5. **Discussion, Limitations, Reproducibility (1.0-1.25 pages)**
   - what Lucia solves
   - where Lucia fails / open limitations
   - reproducibility assets and regeneration path
6. **Conclusion (0.25-0.4 page)**

## E. Mandatory Figure/Table Set

Prepare at minimum:

1. Main system pipeline figure (session-centered architecture)
2. Platform setup/runtime benchmark summary (A)
3. Developer pilot summary (time/errors/effort + SUS/TLX) (B)
4. Video-QA ablation results on the corridor-navigation benchmark (C1)
5. Measurement fusion ablation + grouped condition errors (C2)
6. Claim-evidence matrix table (from `02_claim_evidence_matrix.md`)
7. Failure taxonomy and representative case cards

## F. Required Writing Moves

1. Rename "Case Study 1/2" sections to "Plug-in A/B Evaluation".
2. Move any device/SDK API details that do not support claims into appendix/supplement.
3. For each evaluation subsection, end with:
   - one claim-level takeaway,
   - one explicit boundary statement.
4. Add one final paragraph in discussion titled "Why this is not only integration" that references A+B+C triangulation.
