# run-voice-tests

Execute a voice NLU test set against a classifier and produce a robustness report with aggregate pass/fail/ambiguous statistics.

## Trigger

User says something like:
- `/run-voice-tests`
- "run voice robustness tests"
- "test my voice NLU system"
- "evaluate this voice test set"

## What This Skill Does

Loads a YAML or JSON voice test set, runs each utterance through a classifier (rule-based or LLM), determines pass/fail/ambiguous outcomes, and produces a structured report. Evidence is logged to a JSONL file for tracking over time.

## Step-by-Step Instructions

### Step 1: Locate the Test Set

Ask the user for a test set file path. Accept:
- YAML files (`.yaml` / `.yml`)
- JSON files (`.json`)

If not provided, look for `fixtures/` directory in the workspace and list available test sets.

### Step 2: Validate Test Set Format

YAML format:
```yaml
id: balance_inquiry_v1
description: "Balance inquiry intent tests"
expected_intent: balance_inquiry
utterances:
  - text: "What's my account balance?"
    tags: [clean]
  - text: "check balance"
    tags: [short]
  - text: "um what is my like balance or whatever"
    tags: [disfluent]
```

JSON format:
```json
{
  "id": "support_request_v1",
  "expected_intent": "support_request",
  "utterances": [
    {"text": "I need help", "tags": ["short"]},
    {"text": "please help me with my account", "tags": ["clean"]}
  ]
}
```

Required fields: `id`, `expected_intent`, `utterances` (each with `text`).
If validation fails, report which fields are missing and stop.

### Step 3: Select Classifier

Ask the user: "Which classifier backend? Options: `rule` (keyword-matching, default) or `llm` (requires LLM access)."

Default to `rule`.

**Rule-based classifier:**
- Build a keyword map per intent from the test set's `expected_intent` label
- For each utterance, check for keyword overlap with the intent keywords
- Confidence levels: HIGH (3+ keyword matches), MEDIUM (1-2 matches), LOW (0 matches)
- Outcome: HIGH → expected intent → pass; MEDIUM → check; LOW → ambiguous

**LLM classifier:**
- Prompt: "Classify this utterance into one of these intents: [list intents]. Respond with the intent name and a confidence level (high/medium/low). Utterance: '<text>'"
- Parse response for intent label and confidence
- Compare classified intent to expected_intent

### Step 4: Classify Each Utterance

For each utterance in the test set:

| Field | Value |
|-------|-------|
| text | original utterance text |
| classified_intent | classifier output |
| confidence | high / medium / low |
| outcome | pass / fail / ambiguous |
| tags | from test set |

Outcome rules:
- `pass`: classified_intent == expected_intent AND confidence == high
- `ambiguous`: confidence == medium OR classified_intent is unclear
- `fail`: classified_intent != expected_intent AND confidence == high

### Step 5: Generate Report

```
Voice Robustness Test Report
═══════════════════════════════════════════════════════
Test Set:    <id>
Description: <description>
Expected:    <expected_intent>
Classifier:  <rule|llm>
Run time:    <ISO timestamp>

Results:
  Total utterances: <N>
  Pass:             <N> (<pct>%)
  Fail:             <N> (<pct>%)
  Ambiguous:        <N> (<pct>%)
  Pass rate:        <pct>%

Failures:
  "<utterance text>" → classified as: <intent> (confidence: <level>)
  "<utterance text>" → classified as: <intent> (confidence: <level>)

Ambiguous:
  "<utterance text>" → no clear match (confidence: low)

Tag Breakdown:
  [clean]     <N> utterances: <pass>P / <fail>F / <ambig>A
  [short]     <N> utterances: <pass>P / <fail>F / <ambig>A
  [disfluent] <N> utterances: <pass>P / <fail>F / <ambig>A
```

### Step 6: Append Evidence Log

Append a JSONL entry to `runs/evidence.log.jsonl`:

```json
{
  "timestamp": "<ISO>",
  "test_set_id": "<id>",
  "classifier": "<rule|llm>",
  "total": N,
  "pass": N,
  "fail": N,
  "ambiguous": N,
  "pass_rate": 0.NN,
  "note": "<optional note>"
}
```

## Output Files

- Terminal: full test report
- `runs/evidence.log.jsonl`: appended evidence entry
