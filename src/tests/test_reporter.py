"""Tests for src.report.reporter -- report generation and rendering."""

import json

import pytest

from src.models import ClassificationResult, Outcome
from src.report.reporter import build_report, render_json, render_text, report_to_dict


def _sample_results():
    return [
        ClassificationResult(
            utterance_id="u1",
            text="What's my balance?",
            expected_label="balance_inquiry",
            predicted_label="balance_inquiry",
            outcome=Outcome.PASS,
            confidence=0.9,
        ),
        ClassificationResult(
            utterance_id="u2",
            text="Transfer money",
            expected_label="balance_inquiry",
            predicted_label="transfer_funds",
            outcome=Outcome.FAIL,
        ),
        ClassificationResult(
            utterance_id="u3",
            text="Hmm not sure",
            expected_label="balance_inquiry",
            predicted_label="ambiguous",
            outcome=Outcome.AMBIGUOUS,
            confidence=0.0,
        ),
    ]


class TestBuildReport:
    def test_summary_counts(self):
        report = build_report("ts1", _sample_results())
        assert report.summary.total == 3
        assert report.summary.passes == 1
        assert report.summary.fails == 1
        assert report.summary.ambiguous == 1

    def test_pass_rate(self):
        report = build_report("ts1", _sample_results())
        assert abs(report.summary.pass_rate - 1 / 3) < 0.01

    def test_failed_list(self):
        report = build_report("ts1", _sample_results())
        assert len(report.failed) == 1
        assert report.failed[0].utterance_id == "u2"

    def test_ambiguous_list(self):
        report = build_report("ts1", _sample_results())
        assert len(report.ambiguous_results) == 1
        assert report.ambiguous_results[0].utterance_id == "u3"

    def test_empty_results(self):
        report = build_report("empty", [])
        assert report.summary.total == 0
        assert report.summary.pass_rate == 0.0

    def test_all_pass(self):
        results = [
            ClassificationResult(
                utterance_id="u1",
                text="hi",
                expected_label="a",
                predicted_label="a",
                outcome=Outcome.PASS,
            )
        ]
        report = build_report("perfect", results)
        assert report.summary.passes == 1
        assert report.summary.fails == 0
        assert report.summary.pass_rate == 1.0
        assert len(report.failed) == 0


class TestReportToDict:
    def test_structure(self):
        report = build_report("ts1", _sample_results())
        d = report_to_dict(report)
        assert d["test_set_id"] == "ts1"
        assert "summary" in d
        assert "results" in d
        assert "examples" in d
        assert "failed" in d["examples"]
        assert "ambiguous" in d["examples"]

    def test_pass_rate_rounded(self):
        report = build_report("ts1", _sample_results())
        d = report_to_dict(report)
        assert isinstance(d["summary"]["pass_rate"], float)


class TestRenderJSON:
    def test_valid_json(self):
        report = build_report("ts1", _sample_results())
        raw = render_json(report)
        parsed = json.loads(raw)
        assert parsed["test_set_id"] == "ts1"

    def test_results_count(self):
        report = build_report("ts1", _sample_results())
        parsed = json.loads(render_json(report))
        assert len(parsed["results"]) == 3


class TestRenderText:
    def test_contains_header(self):
        report = build_report("ts1", _sample_results())
        text = render_text(report)
        assert "Robustness Report: ts1" in text

    def test_contains_summary_stats(self):
        report = build_report("ts1", _sample_results())
        text = render_text(report)
        assert "Total utterances" in text
        assert "Passed" in text
        assert "Failed" in text
        assert "Pass rate" in text

    def test_contains_failed_section(self):
        report = build_report("ts1", _sample_results())
        text = render_text(report)
        assert "Failed utterances" in text
        assert "u2" in text

    def test_contains_ambiguous_section(self):
        report = build_report("ts1", _sample_results())
        text = render_text(report)
        assert "Ambiguous utterances" in text
        assert "u3" in text
