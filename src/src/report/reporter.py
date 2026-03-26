"""Robustness report generation.

Aggregates per-utterance classification results into a RobustnessReport
and renders it in JSON or plain-text formats.
"""

from __future__ import annotations

import json
from typing import Any

from src.models import (
    ClassificationResult,
    Outcome,
    ReportSummary,
    RobustnessReport,
)


def build_report(
    test_set_id: str,
    results: list[ClassificationResult],
) -> RobustnessReport:
    """Aggregate a list of results into a RobustnessReport.

    Args:
        test_set_id: Identifier for the test set that was run.
        results: Per-utterance classification results.

    Returns:
        A RobustnessReport with summary counts and highlighted
        failures and ambiguous cases.
    """
    passes = sum(1 for r in results if r.outcome == Outcome.PASS)
    fails = sum(1 for r in results if r.outcome == Outcome.FAIL)
    ambiguous = sum(1 for r in results if r.outcome == Outcome.AMBIGUOUS)

    summary = ReportSummary(
        total=len(results),
        passes=passes,
        fails=fails,
        ambiguous=ambiguous,
    )

    failed = [r for r in results if r.outcome == Outcome.FAIL]
    ambiguous_results = [r for r in results if r.outcome == Outcome.AMBIGUOUS]

    return RobustnessReport(
        test_set_id=test_set_id,
        summary=summary,
        results=results,
        failed=failed,
        ambiguous_results=ambiguous_results,
    )


def report_to_dict(report: RobustnessReport) -> dict[str, Any]:
    """Serialize a RobustnessReport to a plain dict (JSON-ready)."""
    return {
        "test_set_id": report.test_set_id,
        "summary": {
            "total": report.summary.total,
            "passes": report.summary.passes,
            "fails": report.summary.fails,
            "ambiguous": report.summary.ambiguous,
            "pass_rate": round(report.summary.pass_rate, 4),
        },
        "results": [_result_dict(r) for r in report.results],
        "examples": {
            "failed": [_result_dict(r) for r in report.failed],
            "ambiguous": [_result_dict(r) for r in report.ambiguous_results],
        },
    }


def render_json(report: RobustnessReport, indent: int = 2) -> str:
    """Render the report as a JSON string."""
    return json.dumps(report_to_dict(report), indent=indent)


def render_text(report: RobustnessReport) -> str:
    """Render the report as a human-readable text summary."""
    lines: list[str] = []
    s = report.summary
    lines.append(f"=== Robustness Report: {report.test_set_id} ===")
    lines.append("")
    lines.append(f"  Total utterances : {s.total}")
    lines.append(f"  Passed           : {s.passes}")
    lines.append(f"  Failed           : {s.fails}")
    lines.append(f"  Ambiguous        : {s.ambiguous}")
    lines.append(f"  Pass rate        : {s.pass_rate:.1%}")
    lines.append("")

    # Per-utterance table
    lines.append("--- Per-utterance results ---")
    lines.append(
        f"  {'ID':<8} {'Outcome':<12} {'Expected':<20} {'Predicted':<20} Text"
    )
    lines.append("  " + "-" * 80)
    for r in report.results:
        lines.append(
            f"  {r.utterance_id:<8} {r.outcome.value:<12} "
            f"{r.expected_label:<20} {r.predicted_label:<20} "
            f"{r.text[:40]}"
        )
    lines.append("")

    if report.failed:
        lines.append("--- Failed utterances ---")
        for r in report.failed:
            lines.append(
                f"  [{r.utterance_id}] expected={r.expected_label} "
                f"predicted={r.predicted_label} | {r.text}"
            )
        lines.append("")

    if report.ambiguous_results:
        lines.append("--- Ambiguous utterances ---")
        for r in report.ambiguous_results:
            lines.append(
                f"  [{r.utterance_id}] expected={r.expected_label} "
                f"predicted={r.predicted_label} | {r.text}"
            )
        lines.append("")

    return "\n".join(lines)


def _result_dict(r: ClassificationResult) -> dict[str, Any]:
    d: dict[str, Any] = {
        "utterance_id": r.utterance_id,
        "text": r.text,
        "expected_label": r.expected_label,
        "predicted_label": r.predicted_label,
        "outcome": r.outcome.value,
    }
    if r.confidence is not None:
        d["confidence"] = r.confidence
    if r.details:
        d["details"] = r.details
    return d
