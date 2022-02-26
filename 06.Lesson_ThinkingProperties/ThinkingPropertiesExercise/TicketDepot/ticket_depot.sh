certoraRun TicketDepot.sol:TicketDepot --verify TicketDepot:ticket_depot.spec \
--solc solc6.12 \
--msg "$1"

#--rule startOnTime \


# certoraRun verification/harnesses/SymbolicVault.sol verification/harnesses/MultiDistributorHarness.sol \
#   verification/harnesses/SymbolicERC20A.sol verification/harnesses/SymbolicERC20B.sol \
#   --verify MultiDistributorHarness:verification/specs/multiDistributorRules.spec \
