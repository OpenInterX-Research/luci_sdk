"""Pipeline + AI tooling for Lucia reproducible experiments.

This package implements offline-first orchestration for:
- session envelope generation and validation
- package ingestion/analysis workflows
- fixed-path video QA execution
- navigation ablation execution
- reproducibility manifests and claim auditing
"""

from .session import SessionRecord, create_session
from .logger import SessionLogger

__all__ = ["SessionRecord", "create_session", "SessionLogger"]
