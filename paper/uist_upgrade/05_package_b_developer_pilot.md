# Package B Protocol: Developer Productivity Pilot (RQ2)

## Approval Checkpoint (Must Be Filled Before Running)

- Status: `PENDING`
- Objective: measure whether Lucia reduces prototyping friction.
- Required resources:
  - 8 internal participants with Python familiarity
  - task sheets and timing/error logging forms
  - baseline instructions and Lucia instructions
  - SUS and NASA-TLX forms
- Estimated effort: 2 days collection + 1 day analysis
- Claim impact: supports C2 directly and strengthens system-toolkit contribution.
- Approval record:
  - Approved by:
  - Date:
  - Scope notes:

## Study Type

Internal pilot, within-subject, formative evidence.

Default reporting language:

- "internal developer pilot"
- "formative evidence"
- avoid overclaiming broad population generalization

## Design

1. Participants: target N=8
2. Conditions:
   - baseline workflow
   - Lucia workflow
3. Counterbalancing:
   - half baseline-first
   - half Lucia-first

## Tasks

1. Connect, live stream, and save screenshot
2. Record and export a 10s clip
3. Build minimal navigation QA prototype
4. Build minimal measurement prototype

## Measures

### Objective

1. completion time per task
2. task success/failure
3. error count
4. help-request count
5. LOC/config effort proxy

### Subjective

1. SUS score
2. NASA-TLX score
3. single-item confidence to extend to a new app

### Qualitative

Short debrief:

1. top 2 helpful workflow elements
2. top 2 pain points

## Analysis Plan

1. paired nonparametric test for condition differences (Wilcoxon signed-rank)
2. paired effect size (rank-biserial or Cliff-style paired effect report)
3. confidence intervals for key deltas
4. thematic coding for qualitative responses (lightweight, 2-4 themes)

## Acceptance Criteria

1. counterbalancing is respected and logged.
2. no participant has missing objective metrics.
3. each core metric has paired comparison output.
4. at least one limitation is explicit (sample size/internal setting).

