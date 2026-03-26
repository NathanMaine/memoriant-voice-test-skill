"""LLM classifier adapter (scaffold).

This module provides a placeholder for an LLM-backed classifier.
It reads configuration from environment variables and falls back
to returning ``"ambiguous"`` when no LLM service is configured.

To use a real LLM, set the ``LLM_API_KEY`` environment variable and
implement the HTTP/SDK call inside ``predict``.
"""

from __future__ import annotations

import logging
import os

from src.classifier.base import ClassifierResult

logger = logging.getLogger(__name__)


class LLMClassifier:
    """Scaffold LLM classifier that delegates to an external API.

    When ``LLM_API_KEY`` is not set the classifier returns ambiguous
    for every utterance, making it safe to instantiate without
    credentials.
    """

    def __init__(self) -> None:
        self.api_key = os.environ.get("LLM_API_KEY", "")
        if not self.api_key:
            logger.warning(
                "LLM_API_KEY not set; LLMClassifier will return 'ambiguous' "
                "for all utterances. Set the environment variable to enable "
                "real classification."
            )

    def predict(self, text: str, labels: list[str]) -> ClassifierResult:
        """Classify *text* via an LLM prompt.

        Without a configured API key this returns ``"ambiguous"``
        with a note explaining the missing configuration.
        """
        if not self.api_key:
            return ClassifierResult(
                predicted_label="ambiguous",
                confidence=0.0,
                details="LLM_API_KEY not configured; returning ambiguous",
            )

        # --- Real implementation placeholder ---
        # prompt = (
        #     f"Classify the following user utterance into exactly one of "
        #     f"these labels: {', '.join(labels)}.\n\n"
        #     f"Utterance: \"{text}\"\n\n"
        #     f"Respond with only the label."
        # )
        # response = call_llm_api(prompt, self.api_key)
        # predicted = response.strip()
        # return ClassifierResult(predicted_label=predicted, confidence=None)

        return ClassifierResult(
            predicted_label="ambiguous",
            confidence=0.0,
            details="LLM adapter not yet implemented",
        )
