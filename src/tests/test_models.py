"""Tests for src.models data structures."""

from src.models import (
    ClassificationResult,
    EvidenceEntry,
    Outcome,
    ReportSummary,
    RobustnessReport,
    Utterance,
    VoiceTestSet,
)


class TestOutcome:
    def test_values(self):
        assert Outcome.PASS.value == "pass"
        assert Outcome.FAIL.value == "fail"
        assert Outcome.AMBIGUOUS.value == "ambiguous"


class TestUtterance:
    def test_basic_creation(self):
        u = Utterance(id="u1", text="hello")
        assert u.id == "u1"
        assert u.text == "hello"
        assert u.metadata == {}

    def test_with_metadata(self):
        u = Utterance(id="u2", text="hi", metadata={"condition": "noisy"})
        assert u.metadata["condition"] == "noisy"


class TestVoiceTestSet:
    def test_creation(self):
        ts = VoiceTestSet(
            test_set_id="ts1",
            expected_label="greeting",
            utterances=[Utterance(id="u1", text="hello")],
            description="A greeting test set",
        )
        assert ts.test_set_id == "ts1"
        assert ts.expected_label == "greeting"
        assert len(ts.utterances) == 1
        assert ts.description == "A greeting test set"

    def test_default_description(self):
        ts = VoiceTestSet(
            test_set_id="ts2",
            expected_label="x",
            utterances=[],
        )
        assert ts.description == ""


class TestReportSummary:
    def test_pass_rate(self):
        s = ReportSummary(total=10, passes=7, fails=2, ambiguous=1)
        assert s.pass_rate == 0.7

    def test_pass_rate_zero_total(self):
        s = ReportSummary(total=0, passes=0, fails=0, ambiguous=0)
        assert s.pass_rate == 0.0

    def test_perfect_pass_rate(self):
        s = ReportSummary(total=5, passes=5, fails=0, ambiguous=0)
        assert s.pass_rate == 1.0


class TestClassificationResult:
    def test_creation(self):
        r = ClassificationResult(
            utterance_id="u1",
            text="test",
            expected_label="a",
            predicted_label="a",
            outcome=Outcome.PASS,
        )
        assert r.outcome == Outcome.PASS
        assert r.confidence is None
        assert r.details == ""


class TestEvidenceEntry:
    def test_creation(self):
        e = EvidenceEntry(
            timestamp="2025-01-01T00:00:00Z",
            test_set_id="ts1",
            total=4,
            passes=3,
            fails=1,
            ambiguous=0,
            note="test run",
        )
        assert e.test_set_id == "ts1"
        assert e.note == "test run"
