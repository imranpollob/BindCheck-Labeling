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
