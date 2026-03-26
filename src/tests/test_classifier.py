"""Tests for classifier implementations."""

import os

import pytest

from src.classifier.base import ClassifierResult, determine_outcome
from src.classifier.llm_adapter import LLMClassifier
from src.classifier.rule_based import RuleBasedClassifier
from src.models import Outcome


class TestDetermineOutcome:
    def test_pass_exact_match(self):
        assert determine_outcome("greeting", "greeting", None) == Outcome.PASS

    def test_pass_case_insensitive(self):
        assert determine_outcome("Greeting", "greeting", None) == Outcome.PASS

    def test_fail_mismatch(self):
        assert determine_outcome("greeting", "transfer_funds", None) == Outcome.FAIL

    def test_ambiguous_from_label(self):
        assert determine_outcome("greeting", "ambiguous", None) == Outcome.AMBIGUOUS

    def test_ambiguous_low_confidence(self):
        assert determine_outcome("greeting", "transfer_funds", 0.3) == Outcome.AMBIGUOUS

    def test_fail_high_confidence_wrong(self):
        assert determine_outcome("greeting", "transfer_funds", 0.8) == Outcome.FAIL


class TestRuleBasedClassifier:
    @pytest.fixture()
    def clf(self):
        return RuleBasedClassifier()

    def test_balance_inquiry_match(self, clf):
        labels = ["balance_inquiry", "transfer_funds", "support_request"]
        result = clf.predict("What's my balance?", labels)
        assert result.predicted_label == "balance_inquiry"
        assert result.confidence is not None
        assert result.confidence > 0

    def test_support_request_match(self, clf):
        labels = ["balance_inquiry", "transfer_funds", "support_request"]
        result = clf.predict("I need help with my account.", labels)
        assert result.predicted_label == "support_request"

    def test_transfer_funds_match(self, clf):
        labels = ["balance_inquiry", "transfer_funds", "support_request"]
        result = clf.predict("Transfer money to savings.", labels)
        assert result.predicted_label == "transfer_funds"

    def test_no_match_returns_ambiguous(self, clf):
        labels = ["balance_inquiry", "transfer_funds"]
        result = clf.predict("What time is it?", labels)
        assert result.predicted_label == "ambiguous"
        assert result.confidence == 0.0

    def test_custom_keyword_map(self):
        custom = {"pizza": [r"\bpizza\b", r"\bpie\b"]}
        clf = RuleBasedClassifier(keyword_map=custom)
        result = clf.predict("I want a pizza", ["pizza", "salad"])
        assert result.predicted_label == "pizza"

    def test_tie_returns_ambiguous(self):
        custom = {
            "a": [r"\btest\b"],
            "b": [r"\btest\b"],
        }
        clf = RuleBasedClassifier(keyword_map=custom)
        result = clf.predict("this is a test", ["a", "b"])
        assert result.predicted_label == "ambiguous"

    def test_greeting_match(self, clf):
        labels = ["greeting", "balance_inquiry"]
        result = clf.predict("Hello there!", labels)
        assert result.predicted_label == "greeting"


class TestLLMClassifier:
    def test_no_api_key_returns_ambiguous(self, monkeypatch):
        monkeypatch.delenv("LLM_API_KEY", raising=False)
        clf = LLMClassifier()
        result = clf.predict("hello", ["greeting"])
        assert result.predicted_label == "ambiguous"
        assert "not configured" in result.details

    def test_with_fake_key_still_returns_ambiguous(self, monkeypatch):
        """Even with a key set, the scaffold implementation returns ambiguous."""
        monkeypatch.setenv("LLM_API_KEY", "fake-key-12345")
        clf = LLMClassifier()
        result = clf.predict("hello", ["greeting"])
        assert result.predicted_label == "ambiguous"
        assert "not yet implemented" in result.details
