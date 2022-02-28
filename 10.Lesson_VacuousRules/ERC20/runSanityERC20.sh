certoraRun ERC20Fixed.sol:ERC20 --verify ERC20:Sanity.spec \
--solc solc8.0 \
--optimistic_loop \
--send_only \
--msg "$1"