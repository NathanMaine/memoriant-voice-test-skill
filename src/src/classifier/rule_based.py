"""Rule-based keyword classifier.

A simple stub classifier that matches utterance text against keyword
patterns for each label. Useful for offline testing without any
external service dependencies.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from src.classifier.base import ClassifierResult

logger = logging.getLogger(__name__)

# Default keyword map: label -> list of keyword patterns.
# Each pattern is matched case-insensitively anywhere in the utterance text.
DEFAULT_KEYWORD_MAP: dict[str, list[str]] = {
    "balance_inquiry": [
        r"\bbalance\b",
        r"\bhow much\b",
        r"\baccount\b.*\b(left|have|money)\b",
        r"\bmoney\b.*\bhave\b",
    ],
    "transfer_funds": [
        r"\btransfer\b",
        r"\bsend\b.*\bmoney\b",
        r"\bmove\b.*\bfunds\b",
    ],
    "support_request": [
        r"\bhelp\b",
        r"\bsupport\b",
        r"\bproblem\b",
        r"\bissue\b",
        r"\bspeak\b.*\bagent\b",
    ],
    "cancel_service": [
        r"\bcancel\b",
        r"\bterminate\b",
        r"\bend\b.*\b(service|subscription|plan)\b",
    ],
    "greeting": [
        r"\bhello\b",
        r"\bhi\b",
        r"\bhey\b",
        r"\bgood\s+(morning|afternoon|evening)\b",
    ],
}


class RuleBasedClassifier:
    """Keyword-matching classifier with tie-breaking to ambiguous."""

    def __init__(self, keyword_map: dict[str, list[str]] | None = None) -> None:
        self.keyword_map = keyword_map if keyword_map is not None else DEFAULT_KEYWORD_MAP

    def predict(self, text: str, labels: list[str]) -> ClassifierResult:
        """Classify *text* by counting keyword hits per label.

        If exactly one label has the highest score it is returned.
        If multiple labels tie, the result is ``"ambiguous"``.
        If no keywords match any label, the result is ``"ambiguous"``.
        """
        scores: dict[str, int] = {}
        for label in labels:
            patterns = self.keyword_map.get(label, [])
            score = sum(
                1 for pat in patterns if re.search(pat, text, re.IGNORECASE)
            )
            scores[label] = score

        max_score = max(scores.values()) if scores else 0
        if max_score == 0:
            logger.debug("No keyword matches for text: %s", text[:80])
            return ClassifierResult(
                predicted_label="ambiguous",
                confidence=0.0,
                details="no keyword matches",
            )

        top_labels = [l for l, s in scores.items() if s == max_score]
        if len(top_labels) > 1:
            logger.debug("Tie between labels %s for text: %s", top_labels, text[:80])
            return ClassifierResult(
                predicted_label="ambiguous",
                confidence=0.0,
                details=f"tie between {top_labels}",
            )

        winner = top_labels[0]
        total_patterns = len(self.keyword_map.get(winner, [])) or 1
        confidence = max_score / total_patterns

        return ClassifierResult(
            predicted_label=winner,
            confidence=round(confidence, 3),
            details=f"matched {max_score} keyword(s)",
        )
