certoraRun MeetingSchedulerFixed.sol:MeetingScheduler --verify MeetingScheduler:meetings.spec \
--solc solc8.7 \
--send_only \
--rule startOnTime \
--msg "$1"

#--rule startOnTime \