# Labeling protocol amendment (FULL items)

**Date:** 2026-11-23
**Authorized by:** the study author, by phone with rater A ("do whatever you think appropriate and good for the project").
**Changes:** GUIDE.md §5 rule "Do not read the project's source code or diffs" for FULL items only. Everything else in GUIDE.md stands.

## Why

Rater A does not build the tool. With raters walled off from tool development, reading the vulnerable code and the fix gives better ground truth without leaking test cases into the tool, as long as code-derived details stay out of what the tool builder sees before freeze.

## Two-pass protocol (applies to both raters)

### Pass 1: report-only (all 264 items)
- Label exactly as GUIDE.md says, from the report alone. No repo, no commits, no diffs.
- Output: `sheet-rater-A.labeled.csv` (same columns as the original sheet).
- **Pass 1 is the label of record for κ** and for the LIGHT/PSS characterization.
- For FULL items, finish and commit Pass 1 for an item **before** opening its code.

### Pass 2: code-verified (FULL items only, 51)
- Open `repo` at `vuln_commit`, and the diff to `fix_commit` where one exists.
- Output: a **separate** file, `code-review-rater-A.csv`, with columns:
  `item_id, binding_code, pattern_code, c1_code, c2_code, c3_code, changed_from_pass1 (Y/N), code_evidence, fix_addresses_flaw (Y/N/partial/no-fix), confidence_code, minutes_code`
- Pass 1 labels are never edited after the fact. Disagreements live only in the Pass 2 file.

### Test-set hygiene
- Pass 1 notes for FULL items stay at the level of what the report says. No function names, line numbers or diff details.
- `code-review-rater-A.csv` is **not shared with the tool builder until the tool is frozen**. Until then it goes only to the author for adjudication.
- The dev/test split is drawn from the Pass 1 labels with a fixed seed, committed before anyone sees Pass 2.

### Rater B
- Rater B follows the same two passes on their 81 items, so κ can be reported for both report-only and code-verified labels.

## How labels are produced (rater A)

Decided by rater A on 2026-11-23, under the author's go-ahead.

- Claude (AI assistant) goes through every item one at a time, proposes a label, and argues for it with quotes from the report (and from the code for FULL items, in Pass 2).
- Rater A challenges, confirms or overrides. The final label is rater A's call after discussion.
- Each item's discussion log is kept in `discussion/<item_id>.md`.
- The paper's methods section must say "AI-proposed, rater-adjudicated" for rater A's labels.
- Code: FULL items use the pinned `repo`/`vuln_commit`/`fix_commit`. Pass 1 (report only) is written down before the code is opened.

## What to report in the paper
- κ on Pass 1, and κ on Pass 2 for overlapping FULL items.
- How many FULL labels flipped between Pass 1 and Pass 2, and in which direction.
- That the FULL ground truth used for evaluation is the Pass 2 (code-verified) label, adjudicated by the author.
- That 12 of the 51 FULL items have no `fix_commit`, so they add no fixed-version negatives.
