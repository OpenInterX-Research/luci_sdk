# Claim-Evidence Matrix (Fill During Writing)

Use this as a required table in the paper body.

| Claim ID | Claim text | Primary metric(s) | Evidence source | Figure/Table target | Boundary statement (required) | Status |
|---|---|---|---|---|---|---|
| C1 | Lucia provides a unified and reproducible session-centered wearable AI pipeline. | setup success, time-to-first-frame, reconnect behavior, p95 latency, log completeness rate | Package A + schema validation | Fig A1, Fig A2, Tab A1 | Performance degrades under weak Wi-Fi/high loss; recovery cost increases in long runs. | Planned |
| C2 | Lucia reduces developer prototyping friction vs baseline workflows. | completion time, success rate, error/help count, LOC/config effort, SUS, NASA-TLX | Package B within-subject pilot | Fig B1, Tab B1 | Internal pilot scale is limited; external generalization requires larger studies. | Planned |
| C3 | One interface supports egocentric video QA and metric perception through plug-ins. | video-QA answer success, path correctness/followability/hallucination on the corridor-navigation benchmark; measurement MAE, relative error, failure-type distribution | Package C1 + C2 | Fig C1, Fig C2, Tab C1 | Long-horizon or repetitive-corridor video-QA prompts, and reflective/textureless measurement cases, remain failure hotspots. | Planned |

## Validation Rule

Before submission, each row must include:

1. At least one quantitative metric with confidence interval or paired-test output.
2. A concrete figure/table ID that exists in final manuscript.
3. A limitation sentence that is explicit and non-generic.
