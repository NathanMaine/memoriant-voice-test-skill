# Tasks: Voice Robustness Lab (Prototype)

**Input**: SPEC.md + plan.md (000-voice-robustness-lab)
**Prereqs**: Data models defined; rule-based classifier acceptable as default.

## Phase 1: Setup

- [X] T001 Create project layout (`src/classifier`, `src/runner`, `src/report`, `src/cli`, `tests/`, `runs/`).
- [X] T002 Add sample voice test set fixture (YAML and JSON) for smoke runs.
- [X] T003 Configure basic logging + shared typings/model definitions.

## Phase 2: Classifier and Loader

- [X] T010 Implement test set loader supporting YAML + JSON with validation and helpful errors.
- [X] T011 Define classifier interface + enums for `pass`/`fail`/`ambiguous` outcomes.
- [X] T012 Implement rule-based classifier stub (keyword matching, tie → `ambiguous`).
- [X] T013 Scaffold LLM adapter stub (no keys baked in; read config/env; safe fallback when not configured).

## Phase 3: Runner and Reporting

- [X] T020 Implement runner to iterate utterances, call classifier, and produce per-utterance results.
- [X] T021 Aggregate robustness report (totals, pass rate, failed/ambiguous examples).
- [X] T022 Render report in JSON + Markdown/text for CLI output.

## Phase 4: Evidence Logging

- [X] T030 Append JSONL (or CSV) evidence entry per run (timestamp, test_set_id, totals, note/config name).
- [X] T031 Ensure evidence file path is configurable; create parent directories if missing.

## Phase 5: CLI

- [X] T040 CLI command `voice-lab run --test-set <path> --classifier <rule|llm> --log <path>`.
- [X] T041 CLI flags for report format (json/text) and optional note.
- [X] T042 Wire CLI to runner/report/logging; print summary table to stdout.

## Optional (if time allows)

- [ ] T050 Thin HTTP endpoint exposing `/run` to accept test set payload and return report JSON.
