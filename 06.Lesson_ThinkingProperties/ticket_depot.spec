
methods{
    owner() returns (address) envfree
    transactionFee() returns (uint64) envfree
    getEventOwner(uint16) returns (address) envfree
    getRemainingTickets(uint16 )  returns (uint16) envfree

    createEvent(uint64 , uint16 )  returns (uint16 )
    buyNewTicket(uint16 , address )  returns (uint16 )
    offerTicket(uint16 , uint16 , uint64 , address , uint16 )
    buyOfferedTicket(uint16 , uint16 , address ) 

    
}


// Checks that state transition from UNINITIALIZED to PENDING  can only happen if
// createEvent() was called
// rule checkTransitionNonCreatedToCreated(method f, uint16 eventId) {
// 	env e;
// 	calldataarg args;
// 	address ownerBefore = getEventOwner(eventId); 
//     require ownerBefore == 0;
// 	f(e, args);
//     address ownerAfter = getEventOwner(eventId);
// 	assert ownerAfter != 0 => f.selector == createEvent(uint64,uint16).selector , "the owner of changed from 0 to !0 through a function other then createEvent()";
// }

// Checks that state transition from UNINITIALIZED to PENDING  can only happen if
// createEvent() was called
// rule checkDecreasingNumberOfTickets(method f, uint16 eventId) {
// 	env e;
// 	calldataarg args;
// 	address ownerBefore = getEventOwner(eventId);
//     uint16 ticketsBefore = getRemainingTickets(eventId);
//     require ownerBefore != 0;
// 	f(e, args);
//     address ownerAfter = getEventOwner(eventId);
//     uint16 ticketsAfter = getRemainingTickets(eventId);
// 	assert ticketsAfter <= ticketsBefore , "Number of tickets increased!";
// }

rule ownerCannotBeChanged(method f) {
    env e;
    calldataarg args;
    address ownerBefore = owner();
    f(e, args);
    address ownerAfter = owner();
    assert ownerAfter == ownerBefore, "owner changed";
}



// // Checks that state transition from PENDING to STARTED or CANCELLED can only happen if
// // startMeeting() or cancelMeeting() were called, respectively
// rule checkPendingToCancelledOrStarted(method f, uint256 meetingId) {
// 	env e;
// 	calldataarg args;
// 	uint8 stateBefore = getStateById(meetingId);
// 	f(e, args);
//     uint8 stateAfter = getStateById(meetingId);
	
// 	assert (stateBefore == 1 => (stateAfter == 1 || stateAfter == 2 || stateAfter == 4)), "invalidation of the state machine";
// 	assert ((stateBefore == 1 && stateAfter == 2) => f.selector == startMeeting(uint256).selector), "the status of the meeting changed from PENDING to STARTED through a function other then startMeeting()";
// 	assert ((stateBefore == 1 && stateAfter == 4) => f.selector == cancelMeeting(uint256).selector), "the status of the meeting changed from PENDING to CANCELLED through a function other then cancelMeeting()";
// }

// //Checks that state transition from STARTED to ENDED can only happen if endMeeting() was called
// rule checkStartedToStateTransition(method f, uint256 meetingId) {
// 	env e;
// 	calldataarg args;
// 	uint8 stateBefore = getStateById(meetingId);
// 	f(e, args);
//     uint8 stateAfter = getStateById(meetingId);
	
// 	assert (stateBefore == 2 => (stateAfter == 2 || stateAfter == 3)), "the status of the meeting changed from STARTED to an invalid state";
// 	assert ((stateBefore == 2 && stateAfter == 3) => f.selector == endMeeting(uint256).selector), "the status of the meeting changed from STARTED to ENDED through a function other then endMeeting()";
// }




// //Checks that the number of participants in a meeting cannot be decreased
// rule monotonousIncreasingStartAndEndTime(method f, uint256 meetingId) {
// 	env e;
// 	calldataarg args;
//     require getStateById(meetingId) == 0 => getNumOfParticipents(meetingId) == 0;
//     require getStateById(meetingId) == 0 => getStartTimeById(meetingId) == 0;
//     require getStateById(meetingId) == 0 => getEndTimeById(meetingId) == 0;
// 	uint256 startTimeBefore = getStartTimeById(meetingId);
//     uint256 endTimeBefore = getEndTimeById(meetingId);
// 	f(e, args);
//     uint256 startTimeAfter = getStartTimeById(meetingId);
//     uint256 endTimeAfter = getEndTimeById(meetingId);

//     assert startTimeAfter >= startTimeBefore && endTimeAfter >= endTimeBefore, "Wrong variable transition of start or end time";
//     assert (startTimeAfter > startTimeBefore || endTimeAfter > endTimeBefore) => (f.selector == scheduleMeeting(uint256, uint256, uint256).selector), "Wrong variable transition of start or end time";

// }


// //Checks that the number of participants in a meeting cannot be decreased
// rule monotonousIncreasingNumOfParticipants(method f, uint256 meetingId) {
// 	env e;
// 	calldataarg args;
//     require getStateById(meetingId) == 0 => getNumOfParticipents(meetingId) == 0;
// 	uint256 numOfParticipantsBefore = getNumOfParticipents(meetingId);
// 	f(e, args);
//     uint256 numOfParticipantsAfter = getNumOfParticipents(meetingId);

// 	assert numOfParticipantsBefore <= numOfParticipantsAfter, "the number of participants decreased as a result of a function call";
//     assert numOfParticipantsAfter <= 1 +  numOfParticipantsBefore, "wrong increase in number of participants";
//     assert numOfParticipantsBefore < numOfParticipantsAfter => f.selector == joinMeeting(uint256).selector, "wrong functino incresed number of participants";
// }
