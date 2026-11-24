# Notes for the author (rater A)

Collected while labeling. Details are in `discussion/<item>.md`.

## Labeling questions
1. **GUIDE §3 circuit-internal bugs with on-chain impact.** We label them N and tag `[circuit-soundness]` (14 items so far). Confirm, or tell us to flip them as a group. See PROTOCOL.md.
2. **P2 wording:** add "starting/prior state not bound to the consumer's stored state" (L076, L149, L166, L048, L014).
3. **Practical proof-system forgeries** (L234 Linea FS, L085/L233 Scroll aggregation): labeled binding P4 with PSS Y, per §1 + §4 (filter by the PSS column). Theoretical/malleability-only PSS items stay N. As of 2026-11-24 there are 14 items with binding = Y and PSS = Y (L027 L085 L211 L213 L217 L225 L229 L233 L234 L236 L238 L239 L240 L257). Suggestion for the paper: report results both with and without these, since a reviewer may argue a proof-system forgery breaks everything rather than binding specifically. Low-confidence calls carry confidence = L and an alternative in notes, so a sensitivity analysis can flip them.
4. **Unconstrained stored output:** P1 (our choice: L066, L023, L169, L196) or OTHER (as in the guide's Payy example)?

## Data issues in the sheet (FULL items)
- **Vuln commit already contains the fix:** L016 (PrivacyBoost repo is a single squashed commit 7b2a018 that already has the low-order key check; fixes 784a19b etc. not public).
- **Fix commit not public / not reachable:** L012 (0621e84), L029 (54d4d0a), L047 (99e8eec; real fix is squash 22681b1f), L049 (f6f5802, "not our ref").
- **Fix commit not a descendant of vuln commit:** L027 (5776400 vs 094450f, separate branch line).
- **Fix commit doesn't touch the finding:** L041, L051, L002 (Surge 95e7567, only acknowledged); L031 (Boundless 14ee8aa).
- **Partial fixes:** L001 (SAMM suffix match without '@'), L042 (only assessor side), L048 (circuit only, not contract).
- **No ZK in the vulnerable path:** L022 (IBC Eureka Ethereum light client runs natively in CosmWasm).
- **Finding ID mismatches:** L010/L031/L042 (report uses V-BLMP, sheet V-BML); L193/L180 (report V-RISC0, sheet V-BML); L249 (sheet SCRI-1 = PDF SCRI-3); L039/L040/L123/L173 finding_title parsed as "Fix Status: Resolved".
- **Malda finding IDs:** L072/L182 sheet V-MLD-VUL-003/005 = PDF V-MLDZK2-VUL-003/005 (zk-coprocessor V7); L195 sheet V-MLD-VUL-001 = PDF V-MLD2-VUL-001 (lending V6; V-MLD-VUL-001 there is an unrelated liquidation bug).
- **Duplicate source:** two of the three Panther "reports" are the same PDF.
- **Duplicate items:** L112 and L121 are the same ToB finding (TOB-IDEN3-1) from the ToB publication and its zkbugs mirror; L260 and L223 likewise (TOB-IDEN3-2). Rater A labeled each pair identically.
- 12+ FULL items have no fix_commit, so they add no fixed-version negatives.
