certoraRun ThinkingPropertiesExercise/MeetingScheduler/MeetingSchedulerFixed.sol:MeetingScheduler --verify MeetingScheduler:meetings.spec \
--solc solc8.7 \
--optimistic_loop \
--msg "$1"

#--rule startOnTime \


# certoraRun verification/harnesses/SymbolicVault.sol verification/harnesses/MultiDistributorHarness.sol \
#   verification/harnesses/SymbolicERC20A.sol verification/harnesses/SymbolicERC20B.sol \
#   --verify MultiDistributorHarness:verification/specs/multiDistributorRules.spec \
