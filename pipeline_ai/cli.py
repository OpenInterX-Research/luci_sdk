"""CLI entrypoint for Pipeline + AI reproducibility workflows."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .audit import run_claim_audit
from .ingest import ingest_package_a, ingest_package_c2
from .logger import resolve_repo_root
from .manifests import ManifestWriter
from .nav_ablation import run_navigation_ablation
from .package_b import analyze_package_b
from .video_qa_runner import run_video_qa


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Lucia Pipeline + AI runner")
    sub = parser.add_subparsers(dest="command", required=True)

    nav = sub.add_parser("nav-ablation-run", help="Run Package C1 navigation ablations")
    nav.add_argument("--questions-file", required=True, type=Path)
    nav.add_argument("--video-metadata-csv", required=True, type=Path)
    nav.add_argument("--model-path", required=True)
    nav.add_argument("--fallback-model", default="Qwen/Qwen2-VL-2B-Instruct")
    nav.add_argument("--output-root", type=Path, default=Path("."))
    nav.add_argument("--prompt-variants", default="no_anchor,min_anchor,structured_anchor")
    nav.add_argument("--dry-run", action="store_true")
    nav.add_argument("--timeout", type=int, default=300)
    nav.add_argument("--python-cmd", default=sys.executable)
    nav.add_argument("--labels-csv", type=Path)

    vqa = sub.add_parser("video-qa-run", help="Run fixed-path video QA from navigation_task")
    vqa.add_argument("--task", default="corridor_navigation")
    vqa.add_argument("--video")
    vqa.add_argument("--model-preset", choices=["qwen", "st-r1"], default="qwen")
    vqa.add_argument("--dry-run", action="store_true")
    vqa.add_argument("--python-cmd", default=sys.executable)

    pba = sub.add_parser("package-b-analyze", help="Run Package B paired analysis")
    pba.add_argument("--input-csv", required=True, type=Path)
    pba.add_argument("--output-root", type=Path, default=Path("."))

    pia = sub.add_parser("package-a-ingest", help="Validate/ingest Package A template CSV")
    pia.add_argument("--input-csv", required=True, type=Path)
    pia.add_argument("--output-root", type=Path, default=Path("."))

    pic2 = sub.add_parser("package-c2-ingest", help="Validate/ingest Package C2 template CSV")
    pic2.add_argument("--input-csv", required=True, type=Path)
    pic2.add_argument("--output-root", type=Path, default=Path("."))

    audit = sub.add_parser("claim-audit", help="Audit C1/C2/C3 evidence readiness")
    audit.add_argument("--coverage-csv", required=True, type=Path)
    audit.add_argument("--output-root", type=Path, default=Path("."))
    audit.add_argument("--claim-matrix", type=Path)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    repo_root = resolve_repo_root()
    command = "python -m pipeline_ai.cli " + " ".join(sys.argv[1:])

    if args.command == "nav-ablation-run":
        output_root = _resolve_output_root(args, repo_root)
        variants = [v.strip() for v in args.prompt_variants.split(",") if v.strip()]
        result = run_navigation_ablation(
            questions_file=args.questions_file.resolve(),
            metadata_csv=args.video_metadata_csv.resolve(),
            model_path=args.model_path,
            fallback_model=args.fallback_model,
            output_root=output_root,
            prompt_variants=variants,
            dry_run=bool(args.dry_run),
            timeout_s=args.timeout,
            python_cmd=args.python_cmd,
            labels_csv=args.labels_csv.resolve() if args.labels_csv else None,
            command=command,
        )
        _print_outputs(result)
        return 0

    if args.command == "video-qa-run":
        result = run_video_qa(
            task_name=args.task,
            video_name=args.video,
            model_preset=args.model_preset,
            dry_run=bool(args.dry_run),
            python_cmd=args.python_cmd,
            repo_root=repo_root,
        )
        _print_outputs(result)
        return 0

    if args.command == "package-b-analyze":
        output_root = _resolve_output_root(args, repo_root)
        manifest = ManifestWriter(output_root=output_root)
        result = analyze_package_b(
            input_csv=args.input_csv.resolve(),
            output_root=output_root,
            command=command,
            manifest=manifest,
        )
        _print_outputs(result)
        return 0

    if args.command == "package-a-ingest":
        output_root = _resolve_output_root(args, repo_root)
        manifest = ManifestWriter(output_root=output_root)
        result = ingest_package_a(
            input_csv=args.input_csv.resolve(),
            output_root=output_root,
            command=command,
            manifest=manifest,
        )
        _print_outputs(result)
        return 0

    if args.command == "package-c2-ingest":
        output_root = _resolve_output_root(args, repo_root)
        manifest = ManifestWriter(output_root=output_root)
        result = ingest_package_c2(
            input_csv=args.input_csv.resolve(),
            output_root=output_root,
            command=command,
            manifest=manifest,
        )
        _print_outputs(result)
        return 0

    if args.command == "claim-audit":
        output_root = _resolve_output_root(args, repo_root)
        result = run_claim_audit(
            coverage_csv=args.coverage_csv.resolve(),
            output_root=output_root,
            command=command,
            claim_matrix_path=(args.claim_matrix.resolve() if args.claim_matrix else None),
        )
        _print_outputs({"report": result["report_path"]})
        if not result["ok"]:
            print("claim audit failed")
            return 1
        print("claim audit passed")
        return 0

    parser.error(f"unsupported command: {args.command}")
    return 2


def _resolve_output_root(args: argparse.Namespace, repo_root: Path) -> Path:
    output_root = getattr(args, "output_root", Path("."))
    return (output_root if output_root != Path(".") else repo_root).resolve()


def _print_outputs(paths: dict[str, object]) -> None:
    for key, value in paths.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    raise SystemExit(main())
