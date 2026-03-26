# score-robustness

Compute a comprehensive robustness score for a voice NLU system by comparing performance across clean vs. noisy test variants, tag categories, and classifier confidence bands.

## Trigger

User says something like:
- `/score-robustness`
- "score my NLU robustness"
- "how robust is my voice system?"
- "compare clean vs noisy test performance"
- "generate robustness score"

## What This Skill Does

Takes evidence log entries (from `run-voice-tests`) and computes a multi-dimensional robustness score:
1. Overall robustness score (0-100)
2. Per-tag degradation analysis (clean vs. noisy vs. disfluent vs. short)
3. Confidence band analysis (high/medium/low confidence pass rates)
4. Trend analysis across test runs if multiple evidence entries exist
5. Robustness grade (A through F)

## Robustness Score Formula

```
Robustness Score = weighted average of:
  - Clean pass rate                    × 0.20 (baseline)
  - Noise resilience                   × 0.30 (clean_pass_rate / noise_pass_rate)
  - Disfluency resilience              × 0.25 (clean_pass_rate / disfluent_pass_rate)
  - Low-confidence handling            × 0.15 (ambiguous routed correctly)
  - Consistency across runs            × 0.10 (standard deviation of pass rates)

Final score: 0–100
```

## Step-by-Step Instructions

### Step 1: Load Evidence Data

Look for evidence in these locations (in order):
1. Most recent run output passed as argument
2. `runs/evidence.log.jsonl` — all historical runs
3. Ask user for a specific run file

Parse all JSONL entries. Group by test set ID.

### Step 2: Load Detailed Run Results

If the most recent run produced per-utterance results (tagged data), load those for tag-level analysis. Check for `runs/results-<timestamp>.json` files.

### Step 3: Compute Per-Tag Pass Rates

Group utterances by tag and compute pass rate for each:

| Tag | Total | Pass | Fail | Ambiguous | Pass Rate |
|-----|-------|------|------|-----------|-----------|
| clean | N | N | N | N | N% |
| noise:low | N | N | N | N | N% |
| noise:medium | N | N | N | N | N% |
| noise:high | N | N | N | N | N% |
| disfluent | N | N | N | N | N% |
| short | N | N | N | N | N% |
| filler | N | N | N | N | N% |

### Step 4: Compute Degradation Deltas

For each noisy tag, compute degradation vs. clean:

```
noise_degradation = clean_pass_rate - noise_pass_rate
disfluency_degradation = clean_pass_rate - disfluent_pass_rate
```

### Step 5: Compute Robustness Score

Apply the weighted formula. Clamp all components to [0, 100].

### Step 6: Assign Robustness Grade

| Score | Grade | Interpretation |
|-------|-------|----------------|
| 90-100 | A | Production-ready. Highly robust to variation. |
| 80-89 | B | Strong. Minor degradation on extreme noise. |
| 70-79 | C | Acceptable. Noticeable degradation — optimize before production. |
| 60-69 | D | Fragile. High failure rate on noisy/disfluent inputs. |
| < 60 | F | Not robust. Fundamental classification issues. |

### Step 7: Trend Analysis

If 3+ historical runs exist for the same test set ID, compute:
- Pass rate trend (improving, stable, degrading)
- Rolling 3-run average
- Best and worst run

### Step 8: Generate Robustness Score Report

```
Voice NLU Robustness Score Report
═══════════════════════════════════════════════════════
Test Set:     <id>
Runs analyzed: <N>
Last run:      <ISO timestamp>

ROBUSTNESS SCORE: 74/100  Grade: C

Component Scores:
  Clean baseline:          88% pass rate    → 88 pts (×0.20 = 17.6)
  Noise resilience:        71% pass rate    → degradation: 17pp → 71 pts (×0.30 = 21.3)
  Disfluency resilience:   68% pass rate    → degradation: 20pp → 68 pts (×0.25 = 17.0)
  Low-confidence handling: 80% routed right → 80 pts (×0.15 = 12.0)
  Run consistency:         ±4% std dev      → 85 pts (×0.10 = 8.5)

Per-Tag Breakdown:
  [clean]       88%  ████████████████████░░░
  [noise:low]   84%  ████████████████████░░░
  [noise:med]   71%  █████████████████░░░░░░
  [noise:high]  54%  █████████████░░░░░░░░░░
  [disfluent]   68%  ████████████████░░░░░░░
  [short]       79%  ███████████████████░░░░

Recommendations:
  - High noise degradation (34pp drop at high noise) — consider noise-robust preprocessing
  - Disfluency handling is weak — add disfluency examples to classifier training data
  - Short utterances perform well — good disambiguation on minimal context

Trend (last 3 runs):
  Run 1: 69% → Run 2: 71% → Run 3: 74% → IMPROVING ↑
```

## Output Files

- Terminal: full robustness score report
- `runs/robustness-score-<timestamp>.md`: saved report
