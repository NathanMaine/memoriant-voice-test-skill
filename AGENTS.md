# Memoriant Voice Test Skill

Voice NLU robustness testing skills for coding agents.

## Available Skills

### run-voice-tests
Execute a YAML or JSON voice test set against a rule-based or LLM classifier. Produces a structured pass/fail/ambiguous report and appends to the JSONL evidence log.

Skill file: `skills/run-voice-tests/SKILL.md`

### inject-noise
Generate noisy utterance variants from a clean test set: background noise markers, disfluency injection, phrasing mutations, and speed/accent tagging. Expands test coverage without manual authoring.

Skill file: `skills/inject-noise/SKILL.md`

### score-robustness
Compute a weighted robustness score (0-100, grade A-F) from test evidence. Multi-dimensional: clean baseline, noise resilience, disfluency resilience, confidence handling, and run consistency.

Skill file: `skills/score-robustness/SKILL.md`

### review-evidence
Browse, filter, and export the JSONL evidence log. View historical test run summaries, drill into individual runs, detect trends, and prune stale entries.

Skill file: `skills/review-evidence/SKILL.md`

## Available Agents

### voice-test-runner-agent
Test execution and evidence logging agent. Loads test sets, runs utterances through configurable classifiers, and produces structured evidence-backed reports.

Agent file: `agents/voice-test-runner-agent.md`

### robustness-analyst-agent
Deep robustness analysis agent. Computes composite scores from historical evidence, identifies failure patterns, analyzes trends, and produces prioritized improvement recommendations.

Agent file: `agents/robustness-analyst-agent.md`

## Install

```bash
# Claude Code (primary)
/install NathanMaine/memoriant-voice-test-skill

# OpenAI Codex CLI
git clone https://github.com/NathanMaine/memoriant-voice-test-skill.git ~/.codex/skills/voice-test
codex --enable skills

# Google Gemini CLI
gemini extensions install https://github.com/NathanMaine/memoriant-voice-test-skill.git --consent
```

## Source Repository

[NathanMaine/voice-robustness-testing-agent](https://github.com/NathanMaine/voice-robustness-testing-agent)
