"""Test set loader supporting YAML and JSON formats.

Reads a voice test set file, validates required fields, and returns
a VoiceTestSet instance ready for the runner.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import yaml

from src.models import Utterance, VoiceTestSet

logger = logging.getLogger(__name__)


class LoaderError(Exception):
    """Raised when a test set file cannot be loaded or validated."""


def load_test_set(path: str | Path) -> VoiceTestSet:
    """Load a voice test set from a YAML or JSON file.

    Args:
        path: Path to the test set file (.yaml, .yml, or .json).

    Returns:
        A validated VoiceTestSet instance.

    Raises:
        LoaderError: If the file cannot be read, parsed, or is missing
            required fields.
    """
    filepath = Path(path)

    if not filepath.exists():
        raise LoaderError(f"Test set file not found: {filepath}")

    if not filepath.is_file():
        raise LoaderError(f"Path is not a file: {filepath}")

    raw = filepath.read_text(encoding="utf-8")
    suffix = filepath.suffix.lower()

    if suffix in (".yaml", ".yml"):
        data = _parse_yaml(raw, filepath)
    elif suffix == ".json":
        data = _parse_json(raw, filepath)
    else:
        raise LoaderError(
            f"Unsupported file format '{suffix}'. Use .yaml, .yml, or .json."
        )

    return _validate_and_build(data, filepath)


def _parse_yaml(raw: str, filepath: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise LoaderError(f"Failed to parse YAML in {filepath}: {exc}") from exc
    if not isinstance(data, dict):
        raise LoaderError(f"Expected a mapping at top level in {filepath}")
    return data


def _parse_json(raw: str, filepath: Path) -> dict[str, Any]:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise LoaderError(f"Failed to parse JSON in {filepath}: {exc}") from exc
    if not isinstance(data, dict):
        raise LoaderError(f"Expected a mapping at top level in {filepath}")
    return data


def _validate_and_build(data: dict[str, Any], filepath: Path) -> VoiceTestSet:
    """Validate required fields and build a VoiceTestSet."""
    missing = []
    for key in ("test_set_id", "expected_label", "utterances"):
        if key not in data:
            missing.append(key)
    if missing:
        raise LoaderError(
            f"Missing required fields in {filepath}: {', '.join(missing)}"
        )

    raw_utterances = data["utterances"]
    if not isinstance(raw_utterances, list) or len(raw_utterances) == 0:
        raise LoaderError(f"'utterances' must be a non-empty list in {filepath}")

    utterances: list[Utterance] = []
    for idx, item in enumerate(raw_utterances):
        if not isinstance(item, dict):
            raise LoaderError(
                f"Utterance at index {idx} must be a mapping in {filepath}"
            )
        uid = item.get("id")
        text = item.get("text")
        if not uid or not text:
            raise LoaderError(
                f"Utterance at index {idx} missing 'id' or 'text' in {filepath}"
            )
        metadata = item.get("metadata", {})
        if not isinstance(metadata, dict):
            metadata = {}
        utterances.append(Utterance(id=str(uid), text=str(text), metadata=metadata))

    logger.info(
        "Loaded test set '%s' with %d utterances from %s",
        data["test_set_id"],
        len(utterances),
        filepath,
    )

    return VoiceTestSet(
        test_set_id=str(data["test_set_id"]),
        expected_label=str(data["expected_label"]),
        utterances=utterances,
        description=str(data.get("description", "")),
    )
