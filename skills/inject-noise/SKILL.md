# inject-noise

Generate noisy variants of voice utterances: background noise simulation, accent variation markers, speed changes, disfluencies, and phrasing mutations. Augments test sets for robustness evaluation.

## Trigger

User says something like:
- `/inject-noise`
- "create noisy test variants"
- "add noise to my voice test set"
- "augment utterances with variation"
- "test accent and speed robustness"

## What This Skill Does

Takes a clean voice test set and generates a set of augmented utterances with controlled perturbations. Each variant is tagged with its noise type, making it easy to measure which perturbation types degrade classifier accuracy.

## Noise Types

### 1. Background Noise Markers

Simulate transcription artifacts from background noise:

| Noise Level | Effect | Example |
|-------------|--------|---------|
| LOW | Minor word drops | "What's my account balance?" → "What's my account [inaudible]?" |
| MEDIUM | Word substitutions | "What's my account balance?" → "What's my count balance?" |
| HIGH | Multiple drops | "What's [inaudible] account [noise] balance?" |

### 2. Disfluency Injection

Add natural speech disfluencies:

| Type | Pattern | Example |
|------|---------|---------|
| Filler words | Add "um", "uh", "like", "you know" | "um what's my balance" |
| Repetition | Repeat first word/phrase | "what what's my balance" |
| False start | Add abandoned phrase | "I want to— what's my balance" |
| Hedging | Add hedges | "can you maybe tell me my balance or something" |

### 3. Phrasing Mutations

Rephrase the same intent:

| Mutation | Strategy | Example |
|----------|----------|---------|
| Shortening | Drop words | "my balance" |
| Lengthening | Add context | "I was wondering if you could check what my current account balance is" |
| Indirect phrasing | Use indirect question | "do you know what my balance is?" |
| Negation framing | Frame as negation test | "I don't know my balance, can you help?" |

### 4. Accent / Speed Markers

Add metadata tags (these don't change text, they add evaluation context):

| Tag | Meaning |
|-----|---------|
| `[fast]` | Utterance spoken at high speed (transcript may be compressed) |
| `[slow]` | Utterance spoken slowly (may include more filler) |
| `[accent:non-native]` | Possible phoneme-level substitutions |
| `[accent:regional]` | Regional vocabulary variants |

## Step-by-Step Instructions

### Step 1: Load Source Test Set

Ask for a test set file path. Load and validate as per `run-voice-tests`.

### Step 2: Select Noise Configuration

Ask user (or accept defaults):

```
Noise configuration:
  - Background noise: [none / low / medium / high]  (default: medium)
  - Disfluency injection: [none / light / heavy]     (default: light)
  - Phrasing mutations: [N variants per utterance]   (default: 2)
  - Speed/accent tags: [yes / no]                    (default: yes)
```

### Step 3: Generate Variants

For each utterance in the source test set, generate variants:

1. **Original** (always include, tagged `[clean]`)
2. **Noise variant** — apply background noise marker based on configured level
3. **Disfluency variant** — inject one or more disfluency patterns
4. **Phrasing variant(s)** — generate N rephrased versions

Use the following rules for text mutation:
- Filler injection: randomly insert "um", "uh", or "like" before the main verb or noun phrase
- Word drop for noise: replace the last content word with `[inaudible]` at LOW; second-to-last content word at MEDIUM
- Shortening: keep only noun phrase and main verb
- Lengthening: prepend "I was wondering if you could" and append "for me please"

### Step 4: Build Augmented Test Set

Output format:

```yaml
id: <source_id>_augmented_v1
description: "<source description> — augmented with noise injection"
expected_intent: <same as source>
noise_config:
  background: medium
  disfluency: light
  phrasing_variants: 2
utterances:
  - text: "What's my account balance?"
    tags: [clean, original]
    source_id: utt-1
  - text: "What's my account [inaudible]?"
    tags: [noise:medium]
    source_id: utt-1
  - text: "um what's my account balance"
    tags: [disfluent, filler]
    source_id: utt-1
  - text: "my balance"
    tags: [short, phrasing]
    source_id: utt-1
```

### Step 5: Write Output

Write augmented test set to `fixtures/<source_id>_augmented.yaml`.

Print summary:
```
Noise Injection Complete
═════════════════════════════════════
Source:     fixtures/balance_inquiry.yaml
Output:     fixtures/balance_inquiry_augmented.yaml
Original utterances:   <N>
Augmented utterances:  <N>
Expansion factor:      <N>x

Next step: run /run-voice-tests with the augmented file to measure robustness
```

## Output Files

- `fixtures/<source_id>_augmented.yaml`
