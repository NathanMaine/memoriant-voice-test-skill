"""Classifier interface for Voice Robustness Lab.

All classifiers implement the Classifier protocol so the runner
can call them interchangeably.
"""

from __future__ import annotations

from typing import Protocol

from src.models import Outcome


class ClassifierResult:
    """Return value from a classifier's predict method."""

    __slots__ = ("predicted_label", "confidence", "details")

    def __init__(
        self,
        predicted_label: str,
        confidence: float | None = None,
        details: str = "",
    ) -> None:
        self.predicted_label = predicted_label
        self.confidence = confidence
        self.details = details


class Classifier(Protocol):
    """Protocol that every classifier adapter must satisfy."""

    def predict(self, text: str, labels: list[str]) -> ClassifierResult:
        """Classify *text* into one of the provided *labels*.

        Args:
            text: The utterance text to classify.
            labels: Allowed label strings.

        Returns:
            A ClassifierResult with predicted_label, optional confidence,
            and optional details.
        """
        ...


def determine_outcome(expected: str, predicted: str, confidence: float | None) -> Outcome:
    """Map a prediction to an Outcome enum value.

    Rules:
        - If predicted matches expected -> PASS
        - If confidence is not None and below 0.5 -> AMBIGUOUS
        - If predicted == "ambiguous" -> AMBIGUOUS
        - Otherwise -> FAIL
    """
    if predicted.lower() == expected.lower():
        return Outcome.PASS
    if predicted.lower() == "ambiguous":
        return Outcome.AMBIGUOUS
    if confidence is not None and confidence < 0.5:
        return Outcome.AMBIGUOUS
    return Outcome.FAIL
