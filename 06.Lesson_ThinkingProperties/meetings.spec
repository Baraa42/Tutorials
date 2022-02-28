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
    // scheduleMeeting implementation uses msg.sender, info that's encapsulated in the environment
    scheduleMeeting(uint256,uint256,uint256) 
    // startMeeting implementation uses block.timestamp, info that's encapsulated in the environment
    startMeeting(uint256) 
    // cancelMeeting implementation uses msg.sender, info that's encapsulated in the environment
    cancelMeeting(uint256) 
    // endMeeting implementation uses block.timestamp, info that's encapsulated in the environment
    endMeeting(uint256) 
    // joinMeeting implementation does not require any context to get successfully executed
    joinMeeting(uint256) envfree

    
}


// Checks that state transition from UNINITIALIZED to PENDING  can only happen if
// scheduledMeeting() was called
rule checkUninitializedToPending(method f, uint256 meetingId) {
	env e;
	calldataarg args;
	uint8 stateBefore = getStateById(meetingId);
	f(e, args);
    uint8 stateAfter = getStateById(meetingId);
	assert (stateBefore == 0 => (stateAfter == 0 || stateAfter == 1 )), "invalidation of the state machine";
	assert (stateBefore == 0 && stateAfter == 1) => f.selector == scheduleMeeting(uint256,uint256,uint256).selector , "the status of the meeting changed from PENDING to STARTED through a function other then startMeeting()";
}

// Checks that state transition from PENDING to STARTED or CANCELLED can only happen if
// startMeeting() or cancelMeeting() were called, respectively
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

//Checks that state transition from STARTED to ENDED can only happen if endMeeting() was called
rule checkStartedToStateTransition(method f, uint256 meetingId) {
	env e;
	calldataarg args;
	uint8 stateBefore = getStateById(meetingId);
	f(e, args);
    uint8 stateAfter = getStateById(meetingId);
	
	assert (stateBefore == 2 => (stateAfter == 2 || stateAfter == 3)), "the status of the meeting changed from STARTED to an invalid state";
	assert ((stateBefore == 2 && stateAfter == 3) => f.selector == endMeeting(uint256).selector), "the status of the meeting changed from STARTED to ENDED through a function other then endMeeting()";
}




//Checks that the number of participants in a meeting cannot be decreased
rule monotonousIncreasingStartAndEndTime(method f, uint256 meetingId) {
	env e;
	calldataarg args;
    require getStateById(meetingId) == 0 => getNumOfParticipents(meetingId) == 0;
    require getStateById(meetingId) == 0 => getStartTimeById(meetingId) == 0;
    require getStateById(meetingId) == 0 => getEndTimeById(meetingId) == 0;
	uint256 startTimeBefore = getStartTimeById(meetingId);
    uint256 endTimeBefore = getEndTimeById(meetingId);
	f(e, args);
    uint256 startTimeAfter = getStartTimeById(meetingId);
    uint256 endTimeAfter = getEndTimeById(meetingId);

    assert startTimeAfter >= startTimeBefore && endTimeAfter >= endTimeBefore, "Wrong variable transition of start or end time";
    assert (startTimeAfter > startTimeBefore || endTimeAfter > endTimeBefore) => (f.selector == scheduleMeeting(uint256, uint256, uint256).selector), "Wrong variable transition of start or end time";

}


//Checks that the number of participants in a meeting cannot be decreased
rule monotonousIncreasingNumOfParticipants(method f, uint256 meetingId) {
	env e;
	calldataarg args;
    require getStateById(meetingId) == 0 => getNumOfParticipents(meetingId) == 0;
	uint256 numOfParticipantsBefore = getNumOfParticipents(meetingId);
	f(e, args);
    uint256 numOfParticipantsAfter = getNumOfParticipents(meetingId);

	assert numOfParticipantsBefore <= numOfParticipantsAfter, "the number of participants decreased as a result of a function call";
    assert numOfParticipantsAfter <= 1 +  numOfParticipantsBefore, "wrong increase in number of participants";
    assert numOfParticipantsBefore < numOfParticipantsAfter => f.selector == joinMeeting(uint256).selector, "wrong function increased number of participants";
}
