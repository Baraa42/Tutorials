certoraRun PopsicleFinance.sol:PopsicleFinance --verify PopsicleFinance:Popsicle.spec \
--solc solc8.6 \
--optimistic_loop \
--msg "$1" \
--rule totalFunds_GE_to_sum_of_all_funds 