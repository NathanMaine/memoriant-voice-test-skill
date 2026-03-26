"""CLI entry point for Voice Robustness Lab.

Provides the ``voice-lab`` command group with a ``run`` sub-command
that loads a test set, classifies utterances, prints a report, and
appends an evidence log entry.
"""

from __future__ import annotations

import logging
import sys

import click

from src.classifier.llm_adapter import LLMClassifier
from src.classifier.rule_based import RuleBasedClassifier
from src.evidence.logger import append_evidence, create_evidence_entry
from src.report.reporter import build_report, render_json, render_text
from src.runner.loader import LoaderError, load_test_set
from src.runner.runner import run_test_set

DEFAULT_LOG_PATH = "runs/evidence.log.jsonl"


@click.group()
@click.option(
    "-v", "--verbose", is_flag=True, default=False, help="Enable debug logging."
)
def cli(verbose: bool) -> None:
    """Voice Robustness Lab -- test voice/NLU robustness with structured test sets."""
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(levelname)s %(name)s: %(message)s",
        stream=sys.stderr,
    )


@cli.command()
@click.option(
    "--test-set",
    required=True,
    type=click.Path(exists=True),
    help="Path to a voice test set file (YAML or JSON).",
)
@click.option(
    "--classifier",
    type=click.Choice(["rule", "llm"], case_sensitive=False),
    default="rule",
    show_default=True,
    help="Classifier backend to use.",
)
@click.option(
    "--log",
    "log_path",
    type=click.Path(),
    default=DEFAULT_LOG_PATH,
    show_default=True,
    help="Path to the evidence log file (JSONL).",
)
@click.option(
    "--format",
    "report_format",
    type=click.Choice(["text", "json"], case_sensitive=False),
    default="text",
    show_default=True,
    help="Report output format.",
)
@click.option(
    "--note",
    default="",
    help="Optional note to attach to the evidence log entry.",
)
def run(
    test_set: str,
    classifier: str,
    log_path: str,
    report_format: str,
    note: str,
) -> None:
    """Run a voice test set and produce a robustness report."""
    # 1. Load the test set
    try:
        ts = load_test_set(test_set)
    except LoaderError as exc:
        click.echo(f"Error loading test set: {exc}", err=True)
        raise SystemExit(1) from exc

    # 2. Instantiate the classifier
    if classifier == "llm":
        clf = LLMClassifier()
    else:
        clf = RuleBasedClassifier()

    # 3. Run the test set
    results = run_test_set(ts, clf)

    # 4. Build and render report
    report = build_report(ts.test_set_id, results)

    if report_format == "json":
        click.echo(render_json(report))
    else:
        click.echo(render_text(report))

    # 5. Append evidence
    entry = create_evidence_entry(report, note=note or f"classifier={classifier}")
    append_evidence(entry, log_path)
    click.echo(f"\nEvidence logged to {log_path}", err=True)
