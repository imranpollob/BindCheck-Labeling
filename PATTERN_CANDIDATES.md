# Pattern candidates

Shapes that fit the GUIDE patterns awkwardly. Review after the FULL families (~90 items); pitch to the author any shape that recurs 5+ times.

| Candidate | Description | Items | Labeled as |
|---|---|---|---|
| Consumer-filled value | Contract fills in an effect value (amount, etc.) after verification, so the proof's policy checks never see it | L011 | P1 |
| Switch-off policy check (not binding) | Circuit policy check over private witnesses can be disabled; public outputs still honest | L012 | N |
| Skipped consumer safety check (not binding) | Proof fine; consumer skips a guard on one path while choosing among proven candidates | L025, L002 | N |
| Missing freshness check (not binding) | Proven credential reused after expiry | L071 | N |

## Decision line (agreed with rater A, 2026-11-23)
- Binding: the consumer acts on something the proof doesn't lock (public nullifier unpinned, caller-supplied value, amount filled in later, program ID unchecked).
- Not binding: the circuit enforces a rule wrongly, but what the consumer reads is still honestly computed.

## Fail-closed encoding ambiguity (labeled N)
- L032 (timestamp vs slot collapse), L009 (enum mismatch): look like P5, but the mismatch only causes rejection, never a wrong acceptance. Kept as N.

## Open question for the author: GUIDE §3 "circuit-internal under-constraint"
- L036 (EncryptedERC scalar aliasing → withdraw more than balance) and L012 (Panther zone check off via offset=15): huge effect, but every value the consumer reads is fixed by the proof; fix is in-circuit. Labeled N.
- §3 says N only "with no effect on what the consumer is told or acts on". Read literally, these have an effect. Our reading: "told" = a consumer-read value not fixed by the proof. Needs the author's confirmation.
- Decision (rater A, 2026-11-23): binding stays the core label. Confident in-circuit soundness bugs are N and tagged `[circuit-soundness]` in notes (see PROTOCOL.md). Tagged so far: L004 L012 L029 L036 L047 L055 L064 L078 L101.
- Also tagged: L016 (PrivacyBoost), L141 (Scroll). Contrast L027 (Scroll blob FS): consumer's blob commitment is outside the statement → Y/OTHER, not the tag.

## Review after FULL tier (rater A, 2026-11-23; 91 items labeled: 44 Y / 47 N)

Y by pattern: P1 13 · P2 15 · P3 4 · P4 5 · P5 5 · OTHER 2. Only 2 OTHER (L003 parser differential, L027 blob commitment outside the statement), so the five patterns cover the binding class well. **No new pattern proposed.**

Recurring sub-shapes (5+ items or close), all fitting an existing pattern:
1. **Starting/prior state not bound to the consumer's stored state** (P2): L076, L149, L166, L048, L014. P2's text lists chain ID, address, config, domain, but not "prior state". Ask the author to add it to P2's description.
2. **Unconstrained output the consumer stores** (P1): L066, L023, L169, L196. The guide's Payy "extent" example uses OTHER for the same shape. We used P1 ("stored value not fixed"). Ask the author which one; relabel is mechanical (4 items).
3. **Committed config/context hash incomplete** (P2): L119, L179, L100, L050, L074. Fits P2 as written.
4. **Front-running redirects the effect** (P1): L010, L015, L017, L035, L043. Fits P1 + GUIDE §1.
5. **Lossy encoding aliases a value** (P5 when the consumer re-encodes: L089, L013; P3 when it's the replay key: L049). Rule used: pattern follows what the aliased value decides.

Recurring not-binding shapes (labels applied consistently):
- Circuit soundness, consumer-read values locked (tagged): 14 items (L004 L012 L016 L028 L029 L036 L047 L055 L064 L078 L090 L101 L141 L155). Open §3 question above.
- Config pinned by the program/vkey: L104, L152, L148, L096.
- Choosing among fully proven candidates: L025, L002, L033.
- Fails safe: L032, L009.
- Admin/owner config or trust: L031, L037, L084, L034.
- Signature, no proof (§6): L168, L022.
- Off-chain client/watcher gap: L045, L006.
- Proof-system / aggregation layer (PSS Y, binding N): L230, L085, L233, L241.

Pass 1 → Pass 2 flips on FULL: L027 (N → Y, after seeing the blob hash is outside the PI). L031 and L046 leaned Y in the report-only notes but the rater set N for both passes.

## Decision: practical proof-system forgeries (rater A, 2026-11-23)
- A verifier/aggregation flaw that lets a prover forge a meaningful statement is **binding, P4, PSS Y** (GUIDE §1 applied literally; GUIDE §4 says PSS is labeled independently and the author filters later). Items: L234, L085, L233 (+ L209/L259, which are the guide's own P4 list, PSS N).
- Not binding (PSS Y): theoretical or unsteerable issues and malleability: L230, L241, L219, L258, L244, L210.
- Contrast with circuit-internal under-constraint (§3 explicitly excludes): stays N + `[circuit-soundness]`.

## Decision (rater A, 2026-11-24): pass-through vs broken computation
When an in-circuit gap affects a value the consumer stores, rater A separates two shapes:
- **Unauthenticated pass-through → binding (usually P1 stored value).** The stored public output is built from witness data that is never checked against the proved source. Examples: L081 (Lighter master_account_index copied into the exit commitment), L077 (Telepathy committee commitment over unchecked y-coordinates).
- **Broken computation → not binding, `[circuit-soundness]`.** The circuit checks the right data but the arithmetic or gadget is under-constrained, so the prover can prove a false relation. Examples: L070 (Telepathy point doubling), L028, L127/L153 (Intmax BN254 gadgets).
A reviewer may find this line fine-grained; both shapes carry notes so the author can merge them.
