"""Tests for src.evidence.logger -- JSONL evidence logging."""

import json

import pytest

from src.evidence.logger import append_evidence, create_evidence_entry
from src.models import (
    ClassificationResult,
    EvidenceEntry,
    Outcome,
    ReportSummary,
    RobustnessReport,
)


def _sample_report():
    return RobustnessReport(
        test_set_id="test-set",
        summary=ReportSummary(total=4, passes=3, fails=1, ambiguous=0),
        results=[],
    )


class TestCreateEvidenceEntry:
    def test_basic_entry(self):
        report = _sample_report()
        entry = create_evidence_entry(report, note="baseline")
        assert entry.test_set_id == "test-set"
        assert entry.total == 4
        assert entry.passes == 3
        assert entry.fails == 1
        assert entry.ambiguous == 0
        assert entry.note == "baseline"
        assert "T" in entry.timestamp  # ISO format

    def test_empty_note(self):
        entry = create_evidence_entry(_sample_report())
        assert entry.note == ""


class TestAppendEvidence:
    def test_creates_file_and_writes_jsonl(self, tmp_path):
        log_path = tmp_path / "runs" / "evidence.log.jsonl"
        entry = create_evidence_entry(_sample_report(), note="run1")
        append_evidence(entry, log_path)
        assert log_path.exists()

        lines = log_path.read_text().strip().split("\n")
        assert len(lines) == 1
        record = json.loads(lines[0])
        assert record["test_set_id"] == "test-set"
        assert record["total"] == 4
        assert record["note"] == "run1"

    def test_appends_multiple_entries(self, tmp_path):
        log_path = tmp_path / "evidence.jsonl"
        for i in range(3):
            entry = create_evidence_entry(_sample_report(), note=f"run{i}")
            append_evidence(entry, log_path)

        lines = log_path.read_text().strip().split("\n")
        assert len(lines) == 3
        notes = [json.loads(l)["note"] for l in lines]
        assert notes == ["run0", "run1", "run2"]

    def test_creates_parent_dirs(self, tmp_path):
        log_path = tmp_path / "deep" / "nested" / "log.jsonl"
        entry = create_evidence_entry(_sample_report())
        append_evidence(entry, log_path)
        assert log_path.exists()
