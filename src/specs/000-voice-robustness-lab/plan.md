# Implementation Plan: Voice Robustness Lab (Prototype)

**Branch**: `main` | **Date**: 2025-12-12 | **Spec**: `SPEC.md`

## Summary

- Build a small harness that loads text-based voice test sets, routes them through a pluggable classifier/prompt, and produces robustness reports plus an evidence log.
- Prioritize a minimal CLI first; add an optional lightweight HTTP wrapper only if time allows.

## Technical Context

- **Language/Version**: Python 3.11 (adjust if different in this repo)
- **Primary Dependencies**: PyYAML (test set parsing); optional `typer`/`click` for CLI ergonomics
- **Storage**: Local JSONL/CSV for evidence logs in `runs/`
- **Testing**: pytest (smoke/unit around runner, report aggregation)
- **Target Platform**: Local macOS/Linux
- **Project Type**: Single-project CLI/service
- **Constraints**: Keep intents and examples generic; no secrets or vendor-specific flows

## Constitution Check

- Use generic intents and examples (no employer/contact-center specifics).
- Do not embed credentials; allow classifier configuration via environment or config file.
- Keep modules small and explicit (loader, classifier, runner, reporting, evidence logging).

## Project Structure

```text
specs/000-voice-robustness-lab/
├── plan.md
├── tasks.md
└── research.md        # optional, if deeper notes are needed
src/
├── classifier/        # interfaces + rule-based or LLM-backed adapters
├── runner/            # orchestration for running test sets
├── report/            # aggregation + formatting helpers
└── cli/               # CLI entry point
tests/
└── unit/              # smoke/unit coverage for loader, runner, report
runs/
└── evidence.log.jsonl # evidence log output
```

**Structure Decision**: Single-project CLI with swappable classifiers and simple report/log outputs.

## Plan / Phases

- **Phase 0: Foundations** — Define data models (`VoiceTestSet`, `Utterance`, `ClassificationResult`, `RobustnessReport`, `EvidenceEntry`); set up config loading and logging.
- **Phase 1: Classifier interface + baseline** — Implement classifier interface; add a rule-based stub; sketch an LLM adapter with dependency injection.
- **Phase 2: Runner** — Load YAML/JSON test sets; iterate utterances; capture per-utterance results and outcomes (`pass`/`fail`/`ambiguous`).
- **Phase 3: Reporting** — Aggregate counts and pass rate; render JSON and Markdown/text summaries; highlight failures/ambiguous cases.
- **Phase 4: Evidence logging** — Append JSONL/CSV entries per run (timestamp, test_set_id, totals, optional note/config name).
- **Phase 5: CLI** — Command like `voice-lab run --test-set path --classifier rule --log runs/evidence.log.jsonl`; include sample test set fixtures.
- **Phase 6: Optional HTTP** — Thin endpoint to accept test set payloads and return report; only if time remains.

## Risks / Open Questions

- LLM access/keys are out of scope; default to rule-based classifier unless credentials are provided externally.
- Label set is defined by the test set; need validation for empty labels or unknown predictions.
- Ambiguity handling for the rule-based classifier should be explicit (e.g., return `ambiguous` on ties/low confidence).
- YAML vs JSON support: prefer YAML with JSON fallback; document expectations.

## Success Criteria

- CLI runs against a sample test set and emits per-utterance results plus an aggregate summary.
- Evidence log appends one entry per run with timestamp and counts.
- README documents how to run the CLI and where outputs are written.
