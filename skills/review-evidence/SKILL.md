# review-evidence

Review and manage the voice test evidence log: browse historical runs, compare test sets over time, export evidence for compliance or reporting, and clean up stale entries.

## Trigger

User says something like:
- `/review-evidence`
- "show my voice test history"
- "review voice test evidence"
- "export test evidence"
- "what tests have I run?"

## What This Skill Does

Reads the `runs/evidence.log.jsonl` file and provides:
1. Summary table of all historical test runs
2. Filtering by test set ID, date range, classifier type, or pass rate threshold
3. Per-run detailed view
4. CSV export for reporting
5. Evidence log maintenance (prune old entries)

## Step-by-Step Instructions

### Step 1: Load Evidence Log

Read `runs/evidence.log.jsonl`. Parse each line as a JSON object.

If the file doesn't exist or is empty, report:
```
No evidence entries found. Run /run-voice-tests to generate your first test run.
```

### Step 2: Display Summary Table

Show all entries in a summary table, sorted by timestamp (newest first):

```
Voice Test Evidence Log
═══════════════════════════════════════════════════════
Total runs: <N>

Timestamp            │ Test Set ID          │ Classifier │ Pass Rate │ Total
─────────────────────┼──────────────────────┼────────────┼───────────┼──────
2026-03-25 14:32:01  │ balance_inquiry_v1   │ rule       │ 74%       │ 23
2026-03-24 09:15:42  │ support_request_v1   │ llm        │ 88%       │ 17
2026-03-23 16:07:11  │ balance_inquiry_v1   │ rule       │ 71%       │ 23
```

### Step 3: Filter Options

After showing the summary, prompt:
```
Options:
  [1] View details for a specific run
  [2] Filter by test set ID
  [3] Filter by date range
  [4] Show only runs below pass rate threshold
  [5] Export to CSV
  [6] Delete old entries
  [0] Done
```

### Step 4: Detailed Run View

For a selected run, show full entry:

```
Run Details
════════════════════════════════════════
Timestamp:    2026-03-25 14:32:01
Test Set:     balance_inquiry_v1
Classifier:   rule
Note:         experiment-1

Results:
  Total:     23
  Pass:      17 (74%)
  Fail:       4 (17%)
  Ambiguous:  2  (9%)

Evidence entry (raw JSON):
{
  "timestamp": "2026-03-25T14:32:01Z",
  "test_set_id": "balance_inquiry_v1",
  ...
}
```

### Step 5: CSV Export

If user selects export, write `runs/evidence-export-<timestamp>.csv`:

```csv
timestamp,test_set_id,classifier,total,pass,fail,ambiguous,pass_rate,note
2026-03-25T14:32:01Z,balance_inquiry_v1,rule,23,17,4,2,0.739,experiment-1
```

### Step 6: Log Maintenance

If user selects delete, offer options:
- Delete entries older than N days
- Delete entries for a specific test set ID
- Delete entries below a pass rate threshold

Always confirm before deleting:
```
This will delete <N> entries. Type YES to confirm:
```

Write the pruned log back to `runs/evidence.log.jsonl`.

### Step 7: Trend Summary

At the bottom of any multi-run view, show a trend summary:

```
Trend Summary (balance_inquiry_v1):
  Runs: 3  |  Range: 71% - 74%  |  Avg: 72.3%  |  Trend: IMPROVING ↑
```

## Output Files

- Terminal: evidence log display
- `runs/evidence-export-<timestamp>.csv` (if exported)
