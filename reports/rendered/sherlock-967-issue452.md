# Quaint Blonde Aardvark - Malicious operator can alone, with any voting power smaller than quorum forge a proof
URL: https://github.com/sherlock-audit/2025-06-symbiotic-relay-judging/issues/452
Labels: Sponsor Confirmed, Will Fix

Quaint Blonde Aardvark

High

# Malicious operator can alone, with any voting power smaller than quorum forge a proof

### Summary

A malicious operator with any voting power (considering a minimum inclusion voting power if present) smaller than the quorum can forge a proof and bypass verification, setting the next epoch header to any value, taking over the network.
Firstly, in `circuit.go`, operators with keys X, Y equal to 0 are not part of the validator set hash and are [skipped](https://github.com/sherlock-audit/2025-06-symbiotic-relay/blob/main/middleware-sdk/pkg/proof/circuit.go#L94-L98) whenever they are last.
```go
		valsetHash = api.Select(
			api.And(fieldFpApi.IsZero(&circuit.ValidatorData[i].Key.X), fieldFpApi.IsZero(&circuit.ValidatorData[i].Key.Y)),
			valsetHash,
			valsetHashTemp,
		)
```
The reason the X = 0, Y = 0 operators need to be last to be skipped, is because the `valsetHash` takes the temp value when the key is not null. Hence, if we have an empty key (0,0), followed by a non empty key,  valsetHash will take the value of valsetHashTemp again, which includes the full mimc hash, which is cumulative:
```go
		hashAffineG1(&mimcApi, &circuit.ValidatorData[i].Key)
		mimcApi.Write(circuit.ValidatorData[i].VotingPower)
		valsetHashTemp := mimcApi.Sum()
```
Hence, for this to work, the operators must be sent as [OP1, ..., OPn, (0,0)], so `valsetHash` takes the hash of the set up until OPn. It needs to exclude the (0,0) key from the validator set because the MIMC hash is checked against the real hash, which doesn't contain this (0,0) key.

Now, the (0,0) key is not a real operator, so their voting power contribution must be 0. However, it's actually possible to set any voting power (up until var size constraints), exceeding the quorum, of this fake (0,0) validator, and the proof still goes through.

The `IsNonSigner` flag is set to false of this (0,0) validator, so the voting power counts. As a result, their (0,0) key is also added to the signing aggregated key. However, the null (0,0) key point property is that its addition to the aggregate key has no effect, which means that effectively no signature is required from the null (0,0) key. Thus, having validators [OP1, ..., OPn, (0,0)], with an aggregated signature of validators 1 to n, will pass the signature verification.

This effectively means that any operator with any minimal voting power can add this (0,0) operator with a voting power that exceeds the quorum and lets the message go through. As a result, they can manipulate whatever data they want and take full control of the network, more precisely the valSetHeader for the next epoch in `Settlement.sol`, fully compromising the network.

### Root Cause

In `circuit.go:101`, the voting power of an operator with null key must be null.

### Internal Pre-conditions

None

### External Pre-conditions

None

### Attack Path

1. Operator with 1 voting power (or any minimal amount) calls `Settlement::commitValSetHeader()` with a malicious header for next epoch to compromise the network. They send a proof with only them as signer, all other operators are non signers and add at the end a null operator (0,0) with voting power bigger than the quorum.

### Impact

Network is compromised and attacker can do whatever they want. Operator role is permissionless for some networks (depending on extensions) and even if it wasn't, they would still be able to completely bypass the quorum which is high severity.

### PoC

Change `proof_test.go` to:
```go
func genValset(numValidators int, nonSigners []int) []ValidatorData {
	valset := make([]ValidatorData, numValidators)
	for i := 0; i < numValidators; i++ {
		pk := big.NewInt(int64(i + 1000000000000000000))
		valset[i].PrivateKey = pk
		valset[i].Key = getPubkeyG1(pk)
		valset[i].KeyG2 = getPubkeyG2(pk)
		valset[i].VotingPower = big.NewInt(1) // this has to be the real voting power of the rest of the set but it doesn't really matter for this poc as they won't sign. Only validator i == 0 is signing.
		valset[i].IsNonSigner = false
		if i != 0 {
			valset[i].IsNonSigner = true
		}
	}

	for _, nonSigner := range nonSigners {
		valset[nonSigner].IsNonSigner = true
	}

	return valset
}
```

Change `helpers.go` to the following. Note that n is 11 (set has length 10) to add the null key (0,0).
```go
func NormalizeValset(valset []ValidatorData) []ValidatorData {
	// Sort validators by key in ascending order
	sort.Slice(valset, func(i, j int) bool {
		// Compare keys (lower first)
		return valset[i].Key.X.Cmp(&valset[j].Key.X) < 0 || valset[i].Key.Y.Cmp(&valset[j].Key.Y) < 0
	})
	n := 11 //getOptimalN(len(valset))
	normalizedValset := make([]ValidatorData, n)
	for i := range n {
		if i < len(valset) {
			normalizedValset[i] = valset[i]
		} else {
			zeroPoint := new(bn254.G1Affine)
			zeroPoint.SetInfinity()
			zeroPointG2 := new(bn254.G2Affine)
			zeroPointG2.SetInfinity()
			normalizedValset[i] = ValidatorData{PrivateKey: big.NewInt(0), Key: *zeroPoint, KeyG2: *zeroPointG2, VotingPower: big.NewInt(30000000000000 * 10), IsNonSigner: false}
		}
	}
	return normalizedValset
}
```

In `proof.go` set `MaxValidators = []int{11}`. If the 3 verifiers 10, 100, 1000 were used this wouldn't be needed but the current commit defaults to 10 only and it's easier to allow 11 for this POC.

Go to `pkg/proof` and run `go test .`, it passes with 1 real voting power.

### Mitigation

If the key is null, voting power must be null.
