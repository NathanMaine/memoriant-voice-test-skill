"""Test set runner.

Iterates over each utterance in a VoiceTestSet, classifies it,
determines the outcome, and collects per-utterance results.
"""

from __future__ import annotations

import logging

from src.classifier.base import Classifier, ClassifierResult, determine_outcome
from src.models import ClassificationResult, Outcome, VoiceTestSet

logger = logging.getLogger(__name__)


def run_test_set(
    test_set: VoiceTestSet,
    classifier: Classifier,
    extra_labels: list[str] | None = None,
) -> list[ClassificationResult]:
    """Run every utterance in *test_set* through *classifier*.

    Args:
        test_set: The loaded voice test set.
        classifier: Any object satisfying the Classifier protocol.
        extra_labels: Additional labels to include alongside the
            expected label when calling the classifier. Defaults to
            a small set of generic labels if not provided.

    Returns:
        A list of ClassificationResult, one per utterance.
    """
    labels = _build_label_list(test_set.expected_label, extra_labels)
    results: list[ClassificationResult] = []

    for utterance in test_set.utterances:
        logger.debug("Classifying utterance %s: %s", utterance.id, utterance.text[:60])
        try:
            cr: ClassifierResult = classifier.predict(utterance.text, labels)
        except Exception:
            logger.exception("Classifier error for utterance %s", utterance.id)
            cr = ClassifierResult(
                predicted_label="ambiguous",
                confidence=0.0,
                details="classifier raised an exception",
            )

        outcome = determine_outcome(
            expected=test_set.expected_label,
            predicted=cr.predicted_label,
            confidence=cr.confidence,
        )

        results.append(
            ClassificationResult(
                utterance_id=utterance.id,
                text=utterance.text,
                expected_label=test_set.expected_label,
                predicted_label=cr.predicted_label,
                outcome=outcome,
                confidence=cr.confidence,
                details=cr.details,
            )
        )

    logger.info(
        "Finished test set '%s': %d utterances processed",
        test_set.test_set_id,
        len(results),
    )
    return results


def _build_label_list(
    expected: str, extra: list[str] | None
) -> list[str]:
    """Build the label list passed to the classifier.

    Always includes the expected label plus a handful of generic
    distractors so the classifier has something to choose from.
    """
    default_extras = [
        "balance_inquiry",
        "transfer_funds",
        "support_request",
        "cancel_service",
        "greeting",
    ]
    base = extra if extra is not None else default_extras
    labels = list(dict.fromkeys([expected] + base))
    return labels
