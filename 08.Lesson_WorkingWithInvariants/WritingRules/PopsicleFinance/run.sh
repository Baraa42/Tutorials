certoraRun PopsicleFinance.sol:PopsicleFinance --verify PopsicleFinance:Popsicle.spec \
--solc solc8.6 \
--optimistic_loop \
--send_only \
--rule_sanity \
--msg "$1" \
