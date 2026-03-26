# Security Policy

## What This Plugin Does

This plugin consists entirely of markdown instruction files (SKILL.md and agent .md files). It contains:
- No executable code
- No shell scripts
- No network calls
- No file system modifications beyond what Claude Code normally does

All voice test execution, noise injection, and robustness scoring is performed by Claude Code using its standard tools, guided by the skill instructions in this plugin.

## Data Handling

Voice utterance data you provide is processed locally by your AI coding assistant:
- Test set files (YAML/JSON) are read from your local workspace
- Evidence logs are written locally to `runs/evidence.log.jsonl`
- Robustness reports are written to your local `runs/` directory
- No test data or evidence is transmitted to external servers by this plugin

## LLM Classifier Mode

If you use the `--classifier llm` option in `run-voice-tests`, utterance text will be sent to your configured LLM provider as part of a classification prompt. This follows your existing LLM provider's data handling policies. The plugin itself does not make any API calls.

## File Safety

All output is written to `runs/`, `fixtures/`, and `governance-graph/` subdirectories of your current workspace. The plugin never writes outside your workspace.

## Reporting a Vulnerability

If you discover a security issue, please email nathan@memoriant.com (do not open a public issue).

We will respond within 48 hours and provide a fix timeline.

## Auditing This Plugin

This plugin is easy to audit:
1. All files are markdown — readable in any text editor
2. No `node_modules`, no Python packages, no compiled binaries
3. Review any SKILL.md file to see exactly what instructions are given to the AI
4. The `.claude-plugin/plugin.json` lists all skills and agents declared by this plugin
