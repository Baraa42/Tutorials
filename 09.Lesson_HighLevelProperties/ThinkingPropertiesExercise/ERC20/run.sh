certoraRun ERC20Fixed.sol:ERC20 --verify ERC20:ERC20.spec \
--solc solc8.6 \
--optimistic_loop \
--msg "$1" \
--rule balancePreservation 