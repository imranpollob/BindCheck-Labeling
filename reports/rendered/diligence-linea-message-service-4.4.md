# 4.4 Front Running finalizeBlocks When Sequencers Are Decentralized (Major)
Source: https://diligence.security/audits/2023/06/linea-message-service/ (rendered in Chrome 2026-11-23)
Report context: Trust model says "The single sequencer sequences the L2 transaction correctly ... and submits the blocks and proof to L1 timely". Audited commit 8ccf24731c3cd288c27696771c45e4c1a01fa8cc.

## Description
When sequencer is decentralized in the future, one sequencer could front run another sequencer's finalizeBlocks transaction, without doing the actual proving and sequencing, and steal the reward for sequencing if there is one. Once the frontrunner's finalizeBlocks is executed, the original sequencer's transaction would fail as currentL2BlockNumber would increment by one and state root hash won't match, as a result the original sequencer's sequencing and proving work will be wasted.

## Examples
contracts/contracts/ZkEvmV2.sol:L110-L126

```solidity
function finalizeBlocks(
  BlockData[] calldata _blocksData,
  bytes calldata _proof,
  uint256 _proofType,
  bytes32 _parentStateRootHash
)
  external
  whenTypeNotPaused(PROVING_SYSTEM_PAUSE_TYPE)
  whenTypeNotPaused(GENERAL_PAUSE_TYPE)
  onlyRole(OPERATOR_ROLE)
{
  if (stateRootHashes[currentL2BlockNumber] != _parentStateRootHash) {
    revert StartingRootHashDoesNotMatch();
  }

  _finalizeBlocks(_blocksData, _proof, _proofType, _parentStateRootHash, true);
}
```

## Recommendation
Add the sequencer's address as one parameters in _finalizeBlocks function, and include the sequencer's address in the public input hash of the proof in verification function _verifyProof.

```solidity
_verifyProof(
  uint256(
    keccak256(
      abi.encode(
        keccak256(abi.encodePacked(blockHashes)),
        firstBlockNumber,
        keccak256(abi.encodePacked(timestampHashes)),
        keccak256(abi.encodePacked(hashOfRootHashes)),
        keccak256(abi.encodePacked(_sequencer)
      )
    )
  ) % MODULO_R,
  _proofType, _proof, _parentStateRootHash
);
```
