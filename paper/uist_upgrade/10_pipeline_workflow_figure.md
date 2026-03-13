# Figure Asset: Sessionized Pipeline + AI Workflow

Last updated: 2026-03-11
Use this as the figure-ready source for the paper-side workflow diagram.

## Figure Title

**Sessionized Pipeline + AI Workflow**

## Compact Diagram

```text
Package A CSV      Package B CSV      Fixed Task Folder        C1 Metadata/Qs      C2 CSV
(benchmark)        (developer pilot)  + local videos           (ablation)          (measurement)
      \                  |                   |                        |                  /
       \                 |                   |                        |                 /
        +----------------+-------------------+------------------------+----------------+
                                         |
                                         v
                              +----------------------+
                              |      pipeline_ai     |
                              |----------------------|
                              | session creation     |
                              | schema validation    |
                              | fixed-path video QA  |
                              | package analysis     |
                              | manifest logging     |
                              | claim audit          |
                              +----------------------+
                                         |
                  +----------------------+------------------------+------------------+
                  |                      |                        |                  |
                  v                      v                        v                  v
       task result JSONs        validated session logs      tables / figures   claim audit report
       + summary JSON           data/raw/package_*          Tab/Fig A/B/C      submission gate
```

## Figure-Builder Layout

Use a three-column left-to-right figure:

1. **Inputs**
   - Package A benchmark CSV
   - Package B developer-study CSV
   - fixed task folders under `navigation_task/tasks/<task>/`
   - C1 metadata/questions for prompt-variant ablation
   - C2 measurement CSV
2. **Shared Execution Layer**
   - `pipeline_ai`
   - session creation
   - schema validation
   - fixed-path Qwen/ST-R1 video-QA runner
   - package-specific analysis
   - manifest registration
   - claim audit
3. **Outputs**
   - per-video result JSON
   - task summary JSON
   - validated session logs
   - tables and figures
   - claim-audit report

## Short Caption

“Pipeline + AI workflow used in our evaluation. Fixed-path video-QA runs, plug-in ablations, and package-level analyses all pass through a shared sessionized pipeline that validates logs, records manifests, and writes reproducible outputs for manuscript assembly.”

## Long Caption

“Sessionized Pipeline + AI workflow used in the Lucia evaluation. Inputs from benchmark CSVs, developer-study logs, fixed task folders, and plug-in ablation assets all pass through `pipeline_ai`, which standardizes session creation, schema validation, task execution, manifest logging, and claim auditing. The same layer supports fixed-path Qwen-first video QA, prompt-variant C1 ablations, and C2 measurement analysis while producing reproducible task summaries, validated session logs, tables, figures, and a final claim-audit report.”

## Visual Styling Notes

- Make `pipeline_ai` the central largest block.
- Show the fixed task folder as the distinctive input for the video-QA path.
- Use one accent color for shared infrastructure and separate muted colors for A, B, C1, and C2 inputs.
- Label the C1 branch as “video-QA ablation on corridor-navigation benchmark” rather than “navigation module”.
- Keep the output side compact: result JSON, session logs, tables/figures, audit report.
