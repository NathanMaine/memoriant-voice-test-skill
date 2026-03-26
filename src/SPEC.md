# Specification: Voice Robustness Lab (Prototype)

## 1. Problem

Voice and conversational interfaces are often **fragile**:

- Slight changes in phrasing can cause misclassification or wrong routing.
- Background noise, filler words, or accents can confuse NLU pipelines.
- It is hard to reason about robustness without **structured test cases**.

This prototype explores a small **Voice Robustness Lab** that:

- Accepts **voice test sets** (text transcripts + expected intents/routes)
- Runs them through **prompt templates** or simple classification logic
- Produces a **robustness report** with pass/fail/ambiguous stats
- Logs minimal **evidence** for each test run

The goal is to support **quick experiments** around voice robustness, not full speech/NLU infrastructure.

---

## 2. Users and Use Cases

### Users

- **Developers / designers** working on conversational flows who want:
  - A small harness to test “How robust is this intent to phrasing variants?”
- **Experimenters** exploring the impact of prompt tweaks on classification performance.

### Primary use cases (first slice)

1. **Intent robustness check**
   - Input:
     - A test set describing a target intent
     - Several utterance variants (transcribed phrases)
     - Expected label/route
   - Output:
     - Per-utterance classification results
     - Pass/fail/ambiguous metrics

2. **Evidence logging**
   - Each test run appends an evidence entry:
     - Test set identifier
     - When it was run
     - Basic pass/fail stats

---

## 3. Inputs and Outputs

### 3.1 Voice Test Set (Input)

For the first slice, we treat “voice” as **text transcripts** (no raw audio).

A test set can be represented as YAML or JSON with:

- `test_set_id` (string)
- `description` (optional)
- `expected_label` or `expected_route` (string)
- `utterances`: list of objects, e.g.:
  - `id`
  - `text` (transcribed utterance)
  - optional `metadata` (e.g., “noisy”, “fast speech”, etc.)

Example (YAML-ish):

```yaml
test_set_id: "balance-inquiry"
description: "User asking for their account balance."
expected_label: "balance_inquiry"

utterances:
  - id: "u1"
    text: "What's my balance?"
  - id: "u2"
    text: "Can you tell me how much money I have?"
  - id: "u3"
    text: "How much is left in my checking account?"
  - id: "u4"
    text: "Uh, yeah, I just wanna know my account balance, please."
```

### 3.2 Prompt Template / Classifier (Input)

For the first slice, we can use either:

- A simple prompt template that asks an LLM to classify the utterance into a label, or
- A local classifier stub (e.g., keyword-based) that can be swapped out.

Simple classifier interface:

- Input: text
- Output: predicted label (string) and optional confidence

Implementation can live in `src/classifier` and be configured via environment.

### 3.3 Per-Utterance Results (Output)

For each utterance, the tool should produce:

- `utterance_id`
- `text`
- `expected_label`
- `predicted_label`
- `outcome` (`pass` | `fail` | `ambiguous`)
- Optional details (e.g., classifier confidence or reasoning snippet)

Example (JSON-ish):

```json
{
  "utterance_id": "u2",
  "text": "Can you tell me how much money I have?",
  "expected_label": "balance_inquiry",
  "predicted_label": "balance_inquiry",
  "outcome": "pass"
}
```

### 3.4 Robustness Report (Output)

A robustness report aggregates utterance-level results and should include:

- `test_set_id`
- `summary` (total, passes, fails, ambiguous, optional pass_rate)
- Highlighted failures or ambiguous utterances (optional)

Example (JSON-ish):

```json
{
  "test_set_id": "balance-inquiry",
  "summary": {
    "total": 4,
    "passes": 3,
    "fails": 1,
    "ambiguous": 0,
    "pass_rate": 0.75
  },
  "examples": {
    "failed": [
      {
        "utterance_id": "u3",
        "text": "How much is left in my checking account?",
        "expected_label": "balance_inquiry",
        "predicted_label": "transfer_funds"
      }
    ]
  }
}
```

Reports may also be rendered into Markdown or text for CLI output (tables, short summaries, suggested follow-ups).

### 3.5 Evidence Log (Output)

Evidence entries can be stored in JSONL or CSV, containing:

- `timestamp`
- `test_set_id`
- `total`
- `passes`
- `fails`
- `ambiguous`
- Optional `note`

Example JSONL line:

```json
{"timestamp":"2025-01-10T11:15:00Z","test_set_id":"balance-inquiry","total":4,"passes":3,"fails":1,"ambiguous":0,"note":"baseline prompt"}
```

---

## 4. Scope

In scope for the first slice:

- A CLI or simple HTTP endpoint that accepts a test set file (YAML/JSON) and optional classifier/prompt config
- Per-utterance processing via classifier/prompt
- Robustness report generation (structured + human-readable)
- Simple evidence log for test runs

Out of scope for the first slice:

- Handling raw audio or ASR/TTS systems
- Training or fine-tuning models
- Integrations with contact center platforms or telephony

---

## 5. Constraints

- Implemented as a small service or CLI in a common language (e.g., Node/TypeScript or Python)
- Must run locally with minimal setup
- No employer-specific intents, entity names, or call flows
- Test sets and examples must remain generic

---

## 6. Classifier & LLM Use (First Slice)

The initial classifier may be:

- A simple wrapper around an LLM with a prompt like: "Given this user utterance, classify into one of: [label1, label2, ...]."
- A very simple rule-based classifier for offline testing.

Prompt guidance:

- Clearly list allowed labels
- Ask for only the label (and optional confidence/explanation)
- Avoid referencing any real company or product

---

## 7. Minimal Acceptable First Slice

This prototype is considered "working" when:

- A user can run a command or call an endpoint with a test set file
- The tool processes each utterance, produces per-utterance results (expected vs predicted, outcome), and aggregates into a robustness report (pass/fail/ambiguous counts)
- An evidence log entry is appended for each run (timestamp, test set identifier, total/passes/fails/ambiguous)
- README contains basic run instructions

Future enhancements might include:

- Multiple intents per test set
- Configurable label sets and routing rules
- Simple visualization of robustness across multiple test sets
