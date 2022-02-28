
methods{
    owner() returns (address) envfree
    transactionFee() returns (uint64) envfree
    getEventOwner(uint16) returns (address) envfree
    getRemainingTickets(uint16 )  returns (uint16) envfree
    getTicketOwner(uint16 , uint16 ) returns (address) envfree

    createEvent(uint64 , uint16 )  returns (uint16 )
    buyNewTicket(uint16 , address )  returns (uint16 )
    offerTicket(uint16 , uint16 , uint64 , address , uint16 )
    buyOfferedTicket(uint16 , uint16 , address ) 

    
}

// check that owner can never be changed
rule ownerCannotBeChanged(method f) {
    env e;
    calldataarg args;
    address ownerBefore = owner();
    f(e, args);
    address ownerAfter = owner();
    assert ownerAfter == ownerBefore, "owner changed";
}

// Checks that state transition from UNINITIALIZED to PENDING  can only happen if
//createEvent() was called
rule checkTransitionNonCreatedToCreated(method f, uint16 eventId) {
	env e;
	calldataarg args;
	address ownerBefore = getEventOwner(eventId); 
    require ownerBefore == 0;
	f(e, args);
    address ownerAfter = getEventOwner(eventId);
	assert ownerAfter != 0 => f.selector == createEvent(uint64,uint16).selector , "the owner  changed from 0 to !0 through a function other then createEvent()";
}

// Checks that tickets are non decreasing 
rule checkDecreasingNumberOfTickets(method f, uint16 eventId) {
	env e;
	calldataarg args;
	address ownerBefore = getEventOwner(eventId);
    uint16 ticketsBefore = getRemainingTickets(eventId);
    require ownerBefore != 0;
	f(e, args);
    uint16 ticketsAfter = getRemainingTickets(eventId);
	assert ticketsAfter <= ticketsBefore , "Number of tickets increased!";
}

// Checks that tickets remaining decrease only when buyNewTicket is called
rule checkTicketsRemainingChange(method f, uint16 eventId) {
	env e;
	calldataarg args;
	address ownerBefore = getEventOwner(eventId);
    uint16 ticketsBefore = getRemainingTickets(eventId);
    require ownerBefore != 0;
	f(e, args);
    uint16 ticketsAfter = getRemainingTickets(eventId);
	assert ticketsAfter < ticketsBefore => f.selector == buyNewTicket(uint16,address).selector , "Number of tickets increased!";
}

// Checks that tickets owner change only when buyOfferedTicket is called
rule checkTicketsRemainingChange(method f, uint16 eventId, uint16 attendeeId) {
	env e;
	calldataarg args;
    address ownerBefore = getEventOwner(eventId);
	address ticketOwnerBefore = getTicketOwner(eventId, attendeeId);
    require ownerBefore != 0 && ticketOwnerBefore != 0;
	f(e, args);
    address ticketOwnerAfter = getTicketOwner(eventId, attendeeId);
	assert ticketOwnerBefore != ticketOwnerAfter => f.selector == buyOfferedTicket(uint16,uint16,address).selector , "owner illegaly changed!";
}





