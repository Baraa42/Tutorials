certoraRun BankFixed.sol:Bank --verify Bank:invariant.spec \
--solc solc7.6 \
--rule_sanity \
--msg "$1"