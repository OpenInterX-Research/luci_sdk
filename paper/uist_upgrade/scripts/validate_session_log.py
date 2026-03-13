#!/usr/bin/env python3
"""Lightweight validator for Lucia session logs.

Usage:
  python3 validate_session_log.py /path/to/log.json
"""

import json
import sys
from pathlib import Path


REQUIRED_TOP_LEVEL = [
    "session_id",
    "timestamp",
    "device_mode",
    "stream",
    "sync",
    "task",
    "timing_ms",
    "result",
    "failure",
    "env",
]

REQUIRED_NESTED = {
    "stream": [
        "resolution",
        "fps_target",
        "latency_ms",
        "frame_drop_rate",
        "reconnect_count",
        "reconnect_time_ms_p95",
    ],
    "stream.latency_ms": ["mean", "p50", "p95"],
    "sync": ["enabled", "delta_t_ms", "sync_fail_rate"],
    "sync.delta_t_ms": ["mean", "p95"],
    "task": ["type", "query_text", "module_version"],
    "timing_ms": [
        "capture",
        "prompt_build",
        "inference",
        "postprocess",
        "render",
        "end_to_end",
    ],
    "result": ["success", "confidence"],
    "failure": ["failed", "type"],
    "env": ["network_condition", "runtime"],
}


def get_nested(obj, path):
    value = obj
    for part in path.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value


def validate(payload):
    errors = []

    for key in REQUIRED_TOP_LEVEL:
        if key not in payload:
            errors.append(f"missing top-level key: {key}")

    for path, keys in REQUIRED_NESTED.items():
        target = get_nested(payload, path)
        if not isinstance(target, dict):
            errors.append(f"missing object at path: {path}")
            continue
        for key in keys:
            if key not in target:
                errors.append(f"missing key: {path}.{key}")

    if payload.get("device_mode") not in {"USB", "WIFI"}:
        errors.append("device_mode must be USB or WIFI")

    task_type = get_nested(payload, "task.type")
    if task_type not in {"navigation", "measurement", "video_qa"}:
        errors.append("task.type must be navigation, measurement, or video_qa")

    network_condition = get_nested(payload, "env.network_condition")
    if network_condition not in {"normal", "weak", "lossy"}:
        errors.append("env.network_condition must be normal, weak, or lossy")

    return errors


def main():
    if len(sys.argv) != 2:
        print(__doc__.strip())
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"error: file not found: {path}")
        return 2

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"error: failed to parse JSON: {exc}")
        return 2

    errors = validate(payload)
    if errors:
        print("INVALID")
        for err in errors:
            print(f"- {err}")
        return 1

    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
