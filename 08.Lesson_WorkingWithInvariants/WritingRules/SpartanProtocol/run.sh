certoraRun SpartaProtocolPool.sol:SpartaProtocolPool --verify SpartaProtocolPool:Spartan.spec \
--solc solc8.6 \
--optimistic_loop \
--msg "$1" \
--rule tokenAmountDecreaseSameTime 