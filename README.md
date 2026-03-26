<p align="center">
  <img src="https://img.shields.io/badge/claude--code-plugin-8A2BE2" alt="Claude Code Plugin" />
  <img src="https://img.shields.io/badge/skills-4-blue" alt="4 Skills" />
  <img src="https://img.shields.io/badge/agents-2-green" alt="2 Agents" />
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License" />
</p>

# Memoriant Voice Test Skill

A Claude Code plugin for voice NLU robustness testing. Run structured test sets against intent classifiers, inject controlled noise and disfluency, compute weighted robustness scores, and maintain a JSONL evidence log for tracking improvement over time.

**No servers. No Docker. Just install and use.**

## Install

```bash
/install NathanMaine/memoriant-voice-test-skill
```

## Cross-Platform Support

### Claude Code (Primary)
```bash
/install NathanMaine/memoriant-voice-test-skill
```

### OpenAI Codex CLI
```bash
git clone https://github.com/NathanMaine/memoriant-voice-test-skill.git ~/.codex/skills/voice-test
codex --enable skills
```

### Gemini CLI
```bash
gemini extensions install https://github.com/NathanMaine/memoriant-voice-test-skill.git --consent
```

## Skills

| Skill | Command | What It Does |
|-------|---------|-------------|
| **Run Voice Tests** | `/run-voice-tests` | Execute YAML/JSON test sets, produce pass/fail/ambiguous report + JSONL evidence |
| **Inject Noise** | `/inject-noise` | Generate noisy utterance variants: background noise, disfluency, phrasing, speed |
| **Score Robustness** | `/score-robustness` | Weighted robustness score (0-100, grade A-F) across noise type dimensions |
| **Review Evidence** | `/review-evidence` | Browse, filter, export, and maintain the JSONL evidence log |

## Agents

| Agent | Best Model | Specialty |
|-------|-----------|-----------|
| **Voice Test Runner** | Sonnet 4.6 | Test execution, classification, evidence logging |
| **Robustness Analyst** | Opus 4.6 + extended thinking | Score computation, failure pattern analysis, recommendations |

## Quick Start

```bash
# Run a clean test set
/run-voice-tests

# Generate noisy variants to expand coverage
/inject-noise

# Run the augmented test set
/run-voice-tests

# Score robustness across noise types
/score-robustness

# Review historical test results
/review-evidence
```

## Test Set Format

```yaml
id: balance_inquiry_v1
description: "Balance inquiry intent tests"
expected_intent: balance_inquiry
utterances:
  - text: "What's my account balance?"
    tags: [clean]
  - text: "um what is my like balance or whatever"
    tags: [disfluent]
  - text: "check balance"
    tags: [short]
```

## Robustness Score

```
ROBUSTNESS SCORE: 74/100  Grade: C

Component Scores:
  Clean baseline:       88% → 88 pts (×0.20 = 17.6)
  Noise resilience:     71% → 71 pts (×0.30 = 21.3)
  Disfluency resilience: 68% → 68 pts (×0.25 = 17.0)
  Confidence handling:  80% → 80 pts (×0.15 = 12.0)
  Run consistency:      ±4% → 85 pts (×0.10 =  8.5)
```

## Noise Injection Types

| Type | Effect |
|------|--------|
| Background noise | Word drops and substitution artifacts |
| Disfluency | Filler words, repetition, false starts |
| Phrasing mutation | Shortening, lengthening, indirect phrasing |
| Speed/accent tags | Metadata tags for evaluation context |

## Use Cases

- Pre-deployment NLU testing for voice assistants
- Tracking robustness improvements across model versions
- Identifying which noise types break your classifier
- Generating evidence for voice system quality reviews
- Building regression test suites for voice NLU systems

## Using the Actual Tool

The full source code from [NathanMaine/voice-robustness-testing-agent](https://github.com/NathanMaine/voice-robustness-testing-agent) is bundled in `src/` so you can run it directly.

### Install

```bash
# Requires Python 3.10+
cd src
pip install -e ".[dev]"
```

Or install just the runtime dependencies:

```bash
pip install click pyyaml
```

### Run

```bash
# Run a test set from a YAML/JSON file
voice-lab run fixtures/balance_inquiry.yaml

# List available test fixtures
voice-lab list

# Show help
voice-lab --help
```

### Configuration

No configuration file required. Test sets are YAML or JSON files you point the CLI at. Place your own test fixtures anywhere and pass the path to `voice-lab run`.

To use the LLM-backed classifier (instead of the rule-based default), set your provider API key:

```bash
export ANTHROPIC_API_KEY=sk-ant-...   # for Claude
voice-lab run fixtures/balance_inquiry.yaml --classifier llm
```

Evidence logs are written to `runs/` as JSONL files, one entry per utterance result.

### Tests

```bash
pytest
```

### Full Documentation

See the [voice-robustness-testing-agent repo](https://github.com/NathanMaine/voice-robustness-testing-agent) for the complete spec, architecture notes, and contribution guide.

## Source Repository

Built from [NathanMaine/voice-robustness-testing-agent](https://github.com/NathanMaine/voice-robustness-testing-agent).

## License

MIT — see [LICENSE](LICENSE) for details.
