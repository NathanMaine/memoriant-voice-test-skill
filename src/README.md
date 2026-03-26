# Voice Robustness Lab (Prototype)

This repository contains a small, personal proof-of-concept for a **Voice Robustness Lab**.

The goal is to experiment with a helper that can:

- Take **voice utterance transcripts** (and light metadata)
- Exercise **prompt + response patterns** under varied conditions (noise, phrasing, intent)
- Summarize **robustness issues** (e.g., ambiguous intents, brittle prompts, mis-routes)
- Append a minimal **evidence record** for each test run

This is a personal R&D prototype, not a production voice/IVR system.

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### Install

```bash
pip install -e ".[dev]"
```

Or install dependencies directly:

```bash
pip install click pyyaml pytest
```

### Run a Test Set

```bash
# Text report (default)
python -m src.cli.main run --test-set fixtures/balance_inquiry.yaml

# JSON report
python -m src.cli.main run --test-set fixtures/balance_inquiry.yaml --format json

# Use the JSON fixture
python -m src.cli.main run --test-set fixtures/balance_inquiry.json --format json

# With a custom evidence log path and note
python -m src.cli.main run \
  --test-set fixtures/support_request.yaml \
  --log runs/my-evidence.jsonl \
  --note "experiment-1"

# Use the LLM classifier (requires LLM_API_KEY env var; falls back to ambiguous)
python -m src.cli.main run \
  --test-set fixtures/balance_inquiry.yaml \
  --classifier llm

# Verbose mode (debug logging to stderr)
python -m src.cli.main -v run --test-set fixtures/balance_inquiry.yaml
```

### CLI Options

```text
Usage: python -m src.cli.main run [OPTIONS]

Options:
  --test-set PATH          Path to a voice test set file (YAML or JSON). [required]
  --classifier [rule|llm]  Classifier backend to use.  [default: rule]
  --log PATH               Path to the evidence log file (JSONL).  [default: runs/evidence.log.jsonl]
  --format [text|json]     Report output format.  [default: text]
  --note TEXT              Optional note to attach to the evidence log entry.
  --help                   Show this message and exit.
```

### Run Tests

```bash
python -m pytest tests/ -v
```

## Project Structure

```text
src/
  models.py              - Data models (Utterance, VoiceTestSet, ClassificationResult, etc.)
  classifier/
    base.py              - Classifier protocol + outcome determination
    rule_based.py        - Keyword-matching classifier stub
    llm_adapter.py       - LLM classifier scaffold (requires API key)
  runner/
    loader.py            - YAML/JSON test set loader with validation
    runner.py            - Test set runner (iterates utterances through classifier)
  report/
    reporter.py          - Report aggregation + JSON/text rendering
  evidence/
    logger.py            - JSONL evidence log writer
  cli/
    main.py              - Click CLI entry point
fixtures/                - Sample voice test case files
tests/                   - pytest test suite
runs/                    - Evidence log output directory
```

## How It Works

1. **Load** a voice test set (YAML or JSON) describing utterances and an expected intent label.
2. **Classify** each utterance using a pluggable classifier (rule-based keyword matching by default).
3. **Determine outcome** per utterance: `pass` (correct), `fail` (wrong label), or `ambiguous` (low confidence / no match).
4. **Generate a report** with aggregate stats (total, passes, fails, ambiguous, pass rate) and highlighted failures.
5. **Append an evidence entry** (JSONL) with timestamp, test set ID, and counts for tracking over time.

## Non-goals

- End-to-end telephony, ASR, or TTS integration
- Real-time audio capture or streaming
- Full NLU engine or production routing logic

## Status

- [X] Initial specification (`SPEC.md`)
- [X] Minimal flow: voice test set -> prompts/queries -> robustness report
- [X] Evidence log of test runs
- [X] Basic CLI
- [X] Run instructions in README

See `SPEC.md` for the full specification.
