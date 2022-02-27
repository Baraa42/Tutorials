certoraRun BordaFixed.sol:Borda --verify Borda:Borda.spec \
--solc solc7.0 \
--optimistic_loop \
--msg "$1" \
# --rule cannotVoteMoreThanOnce 