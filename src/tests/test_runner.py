"""Tests for src.runner.runner -- test set execution."""

import pytest

from src.classifier.base import ClassifierResult
from src.classifier.rule_based import RuleBasedClassifier
from src.models import Outcome, Utterance, VoiceTestSet
from src.runner.runner import run_test_set


def _make_test_set(utterances=None, expected_label="balance_inquiry"):
    if utterances is None:
        utterances = [
            Utterance(id="u1", text="What's my balance?"),
            Utterance(id="u2", text="Something unrelated entirely."),
        ]
    return VoiceTestSet(
        test_set_id="test-set",
        expected_label=expected_label,
        utterances=utterances,
    )


class TestRunTestSet:
    def test_basic_run(self):
        ts = _make_test_set()
        clf = RuleBasedClassifier()
        results = run_test_set(ts, clf)
        assert len(results) == 2
        assert results[0].utterance_id == "u1"

    def test_all_pass_scenario(self):
        utterances = [
            Utterance(id="u1", text="What's my balance?"),
            Utterance(id="u2", text="Show me my account balance please."),
        ]
        ts = _make_test_set(utterances=utterances)
        clf = RuleBasedClassifier()
        results = run_test_set(ts, clf)
        outcomes = [r.outcome for r in results]
        assert all(o == Outcome.PASS for o in outcomes)

    def test_mixed_outcomes(self):
        utterances = [
            Utterance(id="u1", text="Check my balance"),
            Utterance(id="u2", text="I need to transfer and send money to savings"),
            Utterance(id="u3", text="asdfghjkl"),
        ]
        ts = _make_test_set(utterances=utterances, expected_label="balance_inquiry")
        clf = RuleBasedClassifier()
        results = run_test_set(ts, clf)
        outcomes = {r.utterance_id: r.outcome for r in results}
        assert outcomes["u1"] == Outcome.PASS
        # u2 matches transfer_funds with high confidence (2+ patterns)
        assert outcomes["u2"] == Outcome.FAIL
        assert outcomes["u3"] == Outcome.AMBIGUOUS

    def test_extra_labels_used(self):
        ts = _make_test_set(
            utterances=[Utterance(id="u1", text="hello")],
            expected_label="greeting",
        )
        clf = RuleBasedClassifier()
        results = run_test_set(ts, clf, extra_labels=["greeting", "farewell"])
        assert len(results) == 1
        assert results[0].predicted_label == "greeting"

    def test_classifier_exception_handled(self):
        """If the classifier throws, the runner catches it gracefully."""

        class BrokenClassifier:
            def predict(self, text, labels):
                raise RuntimeError("boom")

        ts = _make_test_set(utterances=[Utterance(id="u1", text="hello")])
        results = run_test_set(ts, BrokenClassifier())
        assert len(results) == 1
        assert results[0].outcome == Outcome.AMBIGUOUS
        assert "exception" in results[0].details
