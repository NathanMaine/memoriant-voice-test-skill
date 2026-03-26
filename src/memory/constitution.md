Constitution for IDE / AI Assistants (Voice Robustness Lab)
This document describes how IDE-integrated AI assistants (e.g., Copilot Chat) should behave when working in this repository.

1. General Rules
Treat this repository as a personal prototype, not a production voice or NLU system.

Avoid generating or suggesting:

Real customer names, company names, or call flows

Internal conversation scripts or contact center designs

Any personally identifiable information beyond generic example names

Use generic intents, phrases, and scenarios (e.g., “balance_inquiry”, “support_request”).

2. Scope of Assistance
AI assistants may help with:

Implementing:

CLI or HTTP endpoints

Test set loaders (YAML/JSON)

Classifier interface and implementations (LLM-backed or rule-based)

Robustness results aggregation and report formatting

Evidence logging (JSONL/CSV)

Designing:

Data models for test sets, utterance results, reports, and evidence entries

Prompt templates for label classification

Writing:

Tests/fixtures for sample test sets

Documentation and usage examples.

AI assistants should not:

Introduce heavy frameworks or audio processing stacks without clear value

Embed API keys or secrets in code

Import real voice scripts or dialogs from actual organizations.

3. Design Preferences
Clear models, for example:

VoiceTestSet

Utterance

ClassificationResult

RobustnessReport

EvidenceEntry

Small, focused modules such as:

testSetLoader

classifier

runner

reportFormatter

evidenceLog

Simple, explicit logging and error handling (e.g., if classification fails or a test set is malformed).

4. Safety & IP
Do not reference employer-specific products, call centers, or internal flows.

Keep examples and intents abstract and generic.

When in doubt, choose conservative, generic designs over detailed replicas of real voice systems.

markdown
Copy code
