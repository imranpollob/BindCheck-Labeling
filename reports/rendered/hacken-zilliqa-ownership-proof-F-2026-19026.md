# Hacken, [SCA] Zilliqa | Zilliqa Ownership Proof | Aug2026 (published Sep 9, 2026), F-2026-19026
Source: https://hacken.io/audits/zilliqa/sca-zilliqa-zilliqa-ownership-proof-aug2026/ (rendered in Chrome 2026-11-24; curl gets a Cloudflare interstitial)

## Context (System Overview, summarized)
Migration of legacy Zilliqa 1.0 accounts after a July 2026 leaf-key leak. A Groth16 circuit proves ownership of a BIP-44 address from the parent node (private witness), so leaked leaf keys are insufficient. Public signals: expectedAddr (claimed legacy address, derived in-circuit), newAddr (migration destination; the overview says "range-checked as a valid 160-bit address"), and a replay-protection domain value.
Contract escrow_v1.sol: lodge() credits deposits to the caller's address; claim() takes a proof and public signals, checks domain matches the current chain, verifies the Groth16 proof, and pays the depositor's balance to the migration destination named in the proof (balance cleared first). lodge() and claim() are permissionless.

## F-2026-19026 Unconstrained newAddr and domain desynchronize the proof from the on-chain address (Medium, Impact 2, Likelihood 1, Fixed in 182ecaa)
Description: newAddr and domain are public inputs, squared only so snarkjs keeps them in the R1CS; neither is otherwise range-checked. expectedAddr is implicitly bounded to 160 bits via address packing; newAddr is not ("newAddr is NOT constrained beyond 'is a field element'").
Recommendation: add Num2Bits(160) (or LessThan 2^160) on newAddr in-circuit.
