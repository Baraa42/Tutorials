/*  Representing enums

    enums are supported by the Certora Verification Language (CVL), 
    according to thier low level representation - uint8.
    in our case:
        -UNINITIALIZED = 0
        -PENDING = 1
        -STARTED = 2
        -ENDED = 3
        -CANCELLED = 4
    So for exmple if we write 'state == 0' we mean 'state == UNINITIALIZED'
    or 'state % 2 == 1' we mean 'state == PENDING || state == ENDED'.

    We will learn more about supported data structures in future lessons.
    For now, follow the above explanation to pass this exercise.
 */

methods{
    // getStateById implementation does not require any context to get successfully executed
    getStateById(uint256) returns (uint8) envfree
    // getStartTimeById implementation does not require any context to get successfully execute
    getStartTimeById(uint256) returns (uint256) envfree
    // getEndTimeById implementation does not require any context to get successfully execute
    getEndTimeById(uint256) returns (uint256) envfree
    // getNumOfParticipents implementation does not require any context to get successfully execute
    getNumOfParticipents(uint256) returns (uint256) envfree
    // getOrganizer implementation does not require any context to get successfully execute
    getOrganizer(uint256) returns (address) envfree
    // scheduleMeeting implementation uses msg.sender, info that's encapsulated in the environment
    scheduleMeeting(uint256,uint256, uint256) 
    // startMeeting implementation uses block.timestamp, info that's encapsulated in the environment
    startMeeting(uint256) 
    // cancelMeeting implementation uses msg.sender, info that's encapsulated in the environment
    cancelMeeting(uint256) 
    // endMeeting implementation uses block.timestamp, info that's encapsulated in the environment
    endMeeting(uint256) 
    // joinMeeting implementation does not require any context to get successfully executed
    joinMeeting(uint256) envfree

    

}

definition meetingUninitialized(uint256 meetingId) returns bool = getStartTimeById(meetingId) == 0 && getEndTimeById(meetingId) == 0 && getNumOfParticipents(meetingId) == 0 && getOrganizer(meetingId) == 0 && getStateById(meetingId) == 0;
definition meetingPending(uint256 meetingId) returns bool = getStartTimeById(meetingId) > 0 && getEndTimeById(meetingId) > 0 && getEndTimeById(meetingId) > getStartTimeById(meetingId) && getNumOfParticipents(meetingId) == 0 && getOrganizer(meetingId) != address(0) && getStateById(meetingId) == 1;
definition meetingStarted(uint256 meetingId) returns bool = getStartTimeById(meetingId) > 0 && getEndTimeById(meetingId) > 0 && getEndTimeById(meetingId) > getStartTimeById(meetingId)  && getOrganizer(meetingId) != address(0) && getStateById(meetingId) == 2;
definition meetingEnded(uint256 meetingId) returns bool = getStartTimeById(meetingId) > 0 && getEndTimeById(meetingId) > 0 && getEndTimeById(meetingId) > getStartTimeById(meetingId)  && getOrganizer(meetingId) != address(0) && getStateById(meetingId) == 3;
definition meetingCancelled(uint256 meetingId) returns bool = getStartTimeById(meetingId) > 0 && getEndTimeById(meetingId) > 0 && getEndTimeById(meetingId) > getStartTimeById(meetingId)  && getOrganizer(meetingId) != address(0) && getStateById(meetingId) == 4;

// Checks that when a meeting is created, the planned end time is greater than the start time
rule startBeforeEnd(method f, uint256 meetingId, uint256 startTime, uint256 endTime) {
	env e;
    scheduleMeeting(e, meetingId, startTime, endTime);
    uint256 scheduledStartTime = getStartTimeById( meetingId);
    uint256 scheduledEndTime = getEndTimeById( meetingId);

	assert scheduledStartTime < scheduledEndTime, "the created meeting's start time is not before its end time";
}


// Checks that a meeting can only be started within the defined range [startTime, endTime]
rule startOnTime(method f, uint256 meetingId) {
	env e;
	calldataarg args;
	uint8 stateBefore = getStateById(meetingId);
	f(e, args); // call only non reverting paths to any function on any arguments.
	uint8 stateAfter = getStateById(meetingId);
    uint256 startTimeAfter = getStartTimeById(meetingId);
    uint256 endTimeAfter = getEndTimeById(meetingId);
    
	assert (stateBefore == 1 && stateAfter == 2) => startTimeAfter <= e.block.timestamp, "started a meeting before the designated starting time.";
	assert (stateBefore == 1 && stateAfter == 2) => endTimeAfter > e.block.timestamp, "started a meeting after the designated end time.";
	
}


// Checks that state transition from STARTED to ENDED can only happen if endMeeting() was called
// @note read again the comment at the top regarding f.selector
rule checkStartedToStateTransition(method f, uint256 meetingId) {
	env e;
	calldataarg args;
	uint8 stateBefore = getStateById(meetingId);
	f(e, args);
    uint8 stateAfter = getStateById(meetingId);
	
	assert (stateBefore == 2 => (stateAfter == 2 || stateAfter == 3)), "the status of the meeting changed from STARTED to an invalid state";
	assert ((stateBefore == 2 && stateAfter == 3) => f.selector == endMeeting(uint256).selector), "the status of the meeting changed from STARTED to ENDED through a function other then endMeeting()";
}


// Checks that state transition from PENDING to STARTED or CANCELLED can only happen if
// startMeeting() or cancelMeeting() were called, respectively
// @note read again the comment at the top regarding f.selector
rule checkPendingToCancelledOrStarted(method f, uint256 meetingId) {
	env e;
	calldataarg args;
	uint8 stateBefore = getStateById(meetingId);
	f(e, args);
    uint8 stateAfter = getStateById(meetingId);
	
	assert (stateBefore == 1 => (stateAfter == 1 || stateAfter == 2 || stateAfter == 4)), "invalidation of the state machine";
	assert ((stateBefore == 1 && stateAfter == 2) => f.selector == startMeeting(uint256).selector), "the status of the meeting changed from PENDING to STARTED through a function other then startMeeting()";
	assert ((stateBefore == 1 && stateAfter == 4) => f.selector == cancelMeeting(uint256).selector), "the status of the meeting changed from PENDING to CANCELLED through a function other then cancelMeeting()";
}


// Checks that the number of participants in a meeting cannot be decreased
rule monotonousIncreasingNumOfParticipants(method f, uint256 meetingId) {
	env e;
	calldataarg args;
    require getStateById(meetingId) == 0 => getNumOfParticipents(meetingId) == 0;
	uint256 numOfParticipantsBefore = getNumOfParticipents(meetingId);
	f(e, args);
    uint256 numOfParticipantsAfter = getNumOfParticipents(meetingId);

	assert numOfParticipantsBefore <= numOfParticipantsAfter, "the number of participants decreased as a result of a function call";
}
