certoraRun PopsicleFinance.sol:PopsicleFinance --verify PopsicleFinance:Popsicle.spec \
--solc solc8.6 \
--optimistic_loop \
--msg "$1" \
--rule supply_GE_single_user_balance 