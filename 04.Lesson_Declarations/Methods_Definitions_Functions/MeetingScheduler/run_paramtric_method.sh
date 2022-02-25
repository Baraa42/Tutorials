certoraRun MeetingSchedulerFixed.sol:MeetingScheduler --verify MeetingScheduler:meetings.spec \
--solc solc8.7 \
--send_only \
--rule startOnTime \
--method "startMeeting(uint256)" \
--msg "$1"

#--rule startOnTime \