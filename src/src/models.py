"""Data models for Voice Robustness Lab.

Defines the core data structures used throughout the system:
- Utterance and VoiceTestSet for test input
- ClassificationResult for per-utterance output
- RobustnessReport and ReportSummary for aggregated results
- EvidenceEntry for the run log
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Any


class Outcome(enum.Enum):
    """Classification outcome for a single utterance."""

    PASS = "pass"
    FAIL = "fail"
    AMBIGUOUS = "ambiguous"


@dataclass
class Utterance:
    """A single voice utterance within a test set."""

    id: str
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class VoiceTestSet:
    """A collection of utterances sharing an expected label."""

    test_set_id: str
    expected_label: str
    utterances: list[Utterance]
    description: str = ""


@dataclass
class ClassificationResult:
    """Result of classifying a single utterance."""

    utterance_id: str
    text: str
    expected_label: str
    predicted_label: str
    outcome: Outcome
    confidence: float | None = None
    details: str = ""


@dataclass
class ReportSummary:
    """Aggregate counts for a robustness report."""

    total: int
    passes: int
    fails: int
    ambiguous: int

    @property
    def pass_rate(self) -> float:
        if self.total == 0:
            return 0.0
        return self.passes / self.total


@dataclass
class RobustnessReport:
    """Full robustness report for a test set run."""

    test_set_id: str
    summary: ReportSummary
    results: list[ClassificationResult]
    failed: list[ClassificationResult] = field(default_factory=list)
    ambiguous_results: list[ClassificationResult] = field(default_factory=list)


@dataclass
class EvidenceEntry:
    """A single evidence log entry for one test run."""

    timestamp: str
    test_set_id: str
    total: int
    passes: int
    fails: int
    ambiguous: int
    note: str = ""
