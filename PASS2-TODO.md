# Pass 2 (code-checked) to-do: 16 newly pinned TEST items

For each item, write a row in `labeling-a/code-review-rater-A.csv` following the same procedure as before (PROTOCOL.md two-pass). Pass 1 is already final. Do not share these with the build lane.

| item | Pass 1 binding | family | finding | repo | vuln | fix |
|---|---|---|---|---|---|---|
| L057 | Y | Hinkal | Missing Domain Separation Enables Conditional Cross-Fork Pro | Hinkal-Protocol/Hinkal-Contracts-Circuits | 306b08253d | 7b8696f86c |
| L089 | Y | RISC Zero / Boundless | On-chain conversion to field elements is incorrect | boundless-xyz/kailua | 6e2ce8f35b | c1aa054e8f |
| L096 | N | RISC Zero / Boundless | Commitment Should Include REVM Version | risc0/risc0-ethereum | 649289a20b |  |
| L107 | N | Hinkal | Emporium Wallet-Mode Signature Authorizes the Operations but | Hinkal-Protocol/Hinkal-Contracts-Circuits | 306b08253d | 2985a07432 |
| L108 | N | Hinkal | EdDSA Verification Does Not Validate Spending Key and Signat | Hinkal-Protocol/Hinkal-Contracts-Circuits | 306b08253d | 62339e220f |
| L119 | Y | RISC Zero / Boundless | Not all fields included in rollup hash | boundless-xyz/kailua | 6e2ce8f35b | c1aa054e8f |
| L144 | N | Hinkal | A Zero `signerAddress` Skips Both the Signature Check and th | Hinkal-Protocol/Hinkal-Contracts-Circuits | 306b08253d | 33810266db |
| L149 | Y | RISC Zero / Boundless | Next Sync Committee Might Be Arbitrarily Set | risc0/r0vm-helios | 87796bbdcc |  |
| L152 | N | RISC Zero / Boundless | Commitment Should Include Execution Environment | risc0/risc0-ethereum | 649289a20b | 7b704888ce |
| L168 | N | RISC Zero / Boundless | No domain separation between client and prover | boundless-xyz/boundless | f0e5fc49c9 | 740adfbc01 |
| L170 | N | Hinkal | Admin Can Configure Security-Critical Changes without Timelo | Hinkal-Protocol/Hinkal-Contracts-Circuits | 306b08253d | ef86e0b3df |
| L172 | Y | RISC Zero / Boundless | Lack of Assurance on Verified Chain Identity | risc0/r0vm-helios | 87796bbdcc | 667f6d5c3a |
| L179 | Y | RISC Zero / Boundless | Incomplete L1 config hash preimage may lead to incorrect | boundless-xyz/kailua | 2414297a5f |  |
| L180 | Y | RISC Zero / Boundless | BoundlessMarket allows delivery of bogus fulfillments | boundless-xyz/boundless | f0e5fc49c9 | fd501d0120 |
| L193 | Y | RISC Zero / Boundless | The BoundlessMarket does not validate RequestIds during | boundless-xyz/boundless | f0e5fc49c9 | fd501d0120 |
| L200 | N | Hinkal | Arbitrary Emporium Calls Allow Theft of Untracked Assets | Hinkal-Protocol/Hinkal-Contracts-Circuits | 306b08253d |  |

## Done (rater A, 2026-11-24)
All 16 rows are in `code-review-rater-A.csv` (now 67 rows), with a Pass 2 section in each `discussion/<item>.md`. AI-proposed, rater-adjudicated, done in the rater-A labeling session, which has not seen tool outputs or the build lane. Pass 1 (sheet) untouched.

- **Result:** no label changes (changed_from_pass1 = N for all 16). Confidence raised to H for L119 and L149, verified in the dependency code: helios-consensus-core 0.8.3 verify_generic_update checks next-period signatures against the store's next_sync_committee (L149); kona 7a40d87 BootInfo loads the rollup config from the oracle for chains outside the registry, and the system-config eip1559 params feed payload attributes (L119; isthmus_time has no effect at that kona rev).
- **code_evidence format:** `path::function | unbound: ... | mechanism`, with repo-relative paths at the vuln commit. The first `path::function` is the primary location; any later `path::function` in the string is a consumer or secondary site (names without `::` are prose, not locations). N rows use `unbound: none (<why>)`. The `[circuit-soundness]` tag (L108) sits in the mechanism part, not in front. L096's location is a struct (`steel/src/lib.rs::Commitment`).
- **Location collisions (one warning could match two items):** L107 and L144 at `EmporiumUpgradeable.sol::verifyWallet`; L149 and L172 at `methods/guest/src/main.rs::main`.

### Data issues for the eval lane
- **Hinkal vuln commit** 306b082 is off `main` and fetches only by full SHA: `306b08253d21c8acfaaf22a5699774e59d773cc7`.
- **Hinkal fix commits** (7b8696f, 2985a07, 62339e2, 3381026, ef86e0b) are not public (the report's source is the private Hinkal-Protocol/Hinkal-Protocol monorepo). Fixes were judged on public `main` 61b6839 (2026-08-31), which moved `hardhat/contracts/` to `contracts/` and `circom/` to `circuits/`. Fixed-version negatives for Hinkal must come from `main` with that layout.
- **L170** mitigation (timelock) is an external deployment contract; no in-repo change.
- **L089/L119:** sheet fix c1aa054 is Release 1.0.0; it contains the report's fix 5586e1d (L089), and the L119 fields, although the report's bd76b76 is not its ancestor.
- **L179:** no sheet fix, but the report's fix a4d3d6b is public and descends from 2414297; it could fill the fix_commit column.
- **L180/L193:** sheet fix fd501d0 ("assorted audit fixes", #465) does not itself touch these; the actual change is f2d7a6c (#441), an ancestor, so code at fd501d0 is fixed.
- **L149:** besides next_sync_committee, the journal's prevHeader/prevHead are never compared with `headers[fromHead]` in R0VMHelios.update (same starting-state mechanism, not a separate finding).
