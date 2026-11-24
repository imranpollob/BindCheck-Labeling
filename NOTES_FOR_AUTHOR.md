# Notes for the author (rater A)

Collected while labeling. Details are in `discussion/<item>.md`.

## Labeling questions
1. **GUIDE §3 circuit-internal bugs with on-chain impact.** We label them N and tag `[circuit-soundness]` (52 items at the end). Confirm, or tell us to flip them as a group. See PROTOCOL.md.
2. **P2 wording:** add "starting/prior state not bound to the consumer's stored state" (L076, L149, L166, L048, L014).
3. **Practical proof-system forgeries** (L234 Linea FS, L085/L233 Scroll aggregation): labeled binding P4 with PSS Y, per §1 + §4 (filter by the PSS column). Theoretical/malleability-only PSS items stay N. As of 2026-11-24 (final) there are 16 items with binding = Y and PSS = Y in the Pass 1 sheet (L085 L204 L211 L213 L217 L222 L225 L229 L233 L234 L236 L238 L239 L240 L255 L257); L027 is binding OTHER + PSS Y in Pass 2 only (code-review-rater-A.csv). Suggestion for the paper: report results both with and without these, since a reviewer may argue a proof-system forgery breaks everything rather than binding specifically. Low-confidence calls carry confidence = L and an alternative in notes, so a sensitivity analysis can flip them.
4. **Unconstrained stored output:** P1 (our choice: L066, L023, L169, L196, L077, L081) or OTHER (as in the guide's Payy example)?
5. **Pass-through vs broken computation** (PATTERN_CANDIDATES.md): a stored output built from witness data never checked against the proved source is binding (L081, L077); an under-constrained computation over the right data is N + `[circuit-soundness]` (L070, L028, Intmax, Tornado MiMC). Confirm this line.
6. **U items (5):** L206, L252, L263, L264 (Sherlock Pico write-ups are in a private repo, GUIDE §6 "source unavailable"; titles suggest Y/P4/PSS Y) and L254 (Spearbit snark-wrapper: public input not exposed, but rated Low with no attack; the report can't settle it).

## Final tally (Pass 1 sheet)
Binding 103 · not binding 156 · U 5. Binding by pattern: OTHER 2, P1 23, P2 23, P3 15, P4 33, P5 7. Confidence: H 83, M 164, L 17.

## Data issues in the sheet (FULL items)
- **Vuln commit already contains the fix:** L016 (PrivacyBoost repo is a single squashed commit 7b2a018 that already has the low-order key check; fixes 784a19b etc. not public).
- **Fix commit not public / not reachable:** L012 (0621e84), L029 (54d4d0a), L047 (99e8eec; real fix is squash 22681b1f), L049 (f6f5802, "not our ref").
- **Fix commit not a descendant of vuln commit:** L027 (5776400 vs 094450f, separate branch line).
- **Fix commit doesn't touch the finding:** L041, L051, L002 (Surge 95e7567, only acknowledged); L031 (Boundless 14ee8aa).
- **Partial fixes:** L001 (SAMM suffix match without '@'), L042 (only assessor side), L048 (circuit only, not contract).
- **No ZK in the vulnerable path:** L022 (IBC Eureka Ethereum light client runs natively in CosmWasm).
- **Finding ID mismatches:** L010/L031/L042 (report uses V-BLMP, sheet V-BML); L193/L180 (report V-RISC0, sheet V-BML); L249 (sheet SCRI-1 = PDF SCRI-3); L039/L040/L123/L173 finding_title parsed as "Fix Status: Resolved".
- **Malda finding IDs:** L072/L182 sheet V-MLD-VUL-003/005 = PDF V-MLDZK2-VUL-003/005 (zk-coprocessor V7); L195 sheet V-MLD-VUL-001 = PDF V-MLD2-VUL-001 (lending V6; V-MLD-VUL-001 there is an unrelated liquidation bug).
- **Webb finding ID:** L109 sheet V-WEB-VUL-005 = PDF V-WBT-VUL-005.
- **Duplicate source:** two of the three Panther "reports" are the same PDF.
- **Duplicate items:** L112 and L121 are the same ToB finding (TOB-IDEN3-1) from the ToB publication and its zkbugs mirror; L260 and L223 likewise (TOB-IDEN3-2). L171 and L201 are the same zk-regex 0xFF bug (Matter Labs report and zk-bug-tracker #27); L087 and L142 are the same circomlib MiMC bug (zkbugs #32 and zk-bug-tracker #14). Rater A labeled each pair identically.
- 12+ FULL items have no fix_commit, so they add no fixed-version negatives.

## Final review (rater A, 2026-11-24)
- **Pass 1 / Pass 2 separation restored.** L027 had its Pass 2 label (Y/OTHER) written into the sheet; PROTOCOL keeps Pass 1 there, so the sheet now holds the report-only label (N, PSS Y) and Pass 2 Y/OTHER stays in code-review-rater-A.csv (changed_from_pass1 = Y). L027 is the only Pass 1 → Pass 2 flip among the 51 FULL items.
- **Test-set hygiene.** 48 of 51 FULL rows had code-derived details (file names, line numbers, commit hashes, "Code-confirmed") in the sheet's notes. These were moved verbatim into each discussion/<item>.md and replaced by a report-level line; code evidence remains in code-review-rater-A.csv. Treat discussion/ as restricted like the code-review file until tool freeze.
- **Pass 2 file completed.** L008, L009, L032, L044 (SP1 Contract Call) were code-reviewed but missing from code-review-rater-A.csv; rows added from their discussion files (all changed_from_pass1 = N).
- **Consistency fixes.** L177 C3 set to met (binding Y requires C1–C3); L095 pattern P3 -> P4 to match L062.
- **Checked and unchanged:** duplicate pairs labeled identically; circuit-soundness tag only on N items with clear in-circuit mechanisms; pass-through outputs (L023, L077, L081, L166, L169, L196) binding; nullifier gaps P3; off-chain/library consumers C2 unclear (13 items); not-binding items flagged "no attack" re-read against GUIDE §6 (label by mechanism): L256 and L254 are the closest calls and keep N and U.
