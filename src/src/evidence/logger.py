"""Evidence log writer.

Appends a JSONL entry for each test run, capturing timestamp,
test set identifier, aggregate counts, and an optional note.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from src.models import EvidenceEntry, RobustnessReport

logger = logging.getLogger(__name__)


def create_evidence_entry(
    report: RobustnessReport,
    note: str = "",
) -> EvidenceEntry:
    """Build an EvidenceEntry from a completed report.

    Args:
        report: The robustness report to summarize.
        note: Free-form note to attach (e.g., classifier name, config).

    Returns:
        An EvidenceEntry ready to be appended to the log.
    """
    return EvidenceEntry(
        timestamp=datetime.now(timezone.utc).isoformat(),
        test_set_id=report.test_set_id,
        total=report.summary.total,
        passes=report.summary.passes,
        fails=report.summary.fails,
        ambiguous=report.summary.ambiguous,
        note=note,
    )


def append_evidence(
    entry: EvidenceEntry,
    log_path: str | Path,
) -> None:
    """Append a single evidence entry as a JSONL line.

    Creates parent directories if they do not exist.

    Args:
        entry: The evidence entry to persist.
        log_path: Path to the JSONL evidence log file.
    """
    filepath = Path(log_path)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "timestamp": entry.timestamp,
        "test_set_id": entry.test_set_id,
        "total": entry.total,
        "passes": entry.passes,
        "fails": entry.fails,
        "ambiguous": entry.ambiguous,
        "note": entry.note,
    }

    line = json.dumps(record, separators=(",", ":"))
    with filepath.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")

    logger.info("Evidence entry appended to %s", filepath)
