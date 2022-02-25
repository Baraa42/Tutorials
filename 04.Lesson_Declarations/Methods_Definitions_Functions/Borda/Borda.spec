
methods{
    // getFullVoterDetails implementation does not require any context to get successfully executed
    getFullVoterDetails(address) returns (uint8, bool, bool, uint256, bool) envfree
    // getFullContenderDetails implementation does not require any context to get successfully execute
    getFullContenderDetails(address) returns (uint8, bool, uint256) envfree
    // getPointsOfContender implementation does not require any context to get successfully executed
    getPointsOfContender(address) returns (uint256) envfree
    // registerVoter's implementation uses msg.sender, info that's encapsulated in the environment
    registerVoter(uint8) returns (bool)
    hasVoted(address) returns (bool) envfree
    getWinner() returns (address, uint256) envfree
    registerContender(uint8) returns (bool)
    vote(address, address, address) returns(bool)
    
}

definition unRegisteredVoter(address voter) returns bool = voterAge(voter) == 0 && !voterRegistered(voter) && !voterVoted(voter) && voterAttempts(voter) == 0 && !voterBlocked(voter);
definition registeredYetVotedVoter(address voter) returns bool = voterRegistered(voter) && !voterVoted(voter) && voterAttempts(voter) == 0 && !voterBlocked(voter);
definition legitRegisteredVotedVoter(address voter) returns bool = voterRegistered(voter) && voterVoted(voter) && voterAttempts(voter) > 0 && voterAttempts(voter) < 3 && !voterBlocked(voter);
definition blockedVoter(address voter) returns bool = voterRegistered(voter) && voterVoted(voter) && voterAttempts(voter) >= 3 && voterBlocked(voter);


function voterAge(address voter) returns uint8 {
    uint8 age; bool voterReg; bool voted; uint256 vote_attempts; bool blocked;
    age, voterReg, voted, vote_attempts, blocked = getFullVoterDetails(voter);
    return age;

}
function voterRegistered(address voter) returns bool {
    uint256 age; bool voterReg; bool voted; uint256 vote_attempts; bool blocked;
    age, voterReg, voted, vote_attempts, blocked = getFullVoterDetails(voter);
    return voterReg;
    
}

function voterVoted(address voter) returns bool {
    uint256 age; bool voterReg; bool voted; uint256 vote_attempts; bool blocked;
    age, voterReg, voted, vote_attempts, blocked = getFullVoterDetails(voter);
    return voted;   
}

function voterAttempts(address voter) returns uint256 {
    uint8 age; bool voterReg; bool voted; uint256 vote_attempts; bool blocked;
    age, voterReg, voted, vote_attempts, blocked = getFullVoterDetails(voter);
    return vote_attempts;
}

function voterBlocked(address voter) returns bool {
    uint256 age; bool voterReg; bool voted; uint256 vote_attempts; bool blocked;
    age, voterReg, voted, vote_attempts, blocked = getFullVoterDetails(voter);
    return blocked;   
}

// Checks that a voter's "registered" mark is changed correctly - 
// If it's false after a function call, it was false before
// If it's true after a function call, it either started as true or changed from false to true via registerVoter()
rule registeredCannotChangeOnceSet(method f, address voter){
    env e; calldataarg args;
    //uint256 age; bool voterRegBefore; bool voted; uint256 vote_attempts; bool blocked;
    //age, voterRegBefore, voted, vote_attempts, blocked = getFullVoterDetails(voter);
    bool voterRegBefore = voterRegistered(voter);
    f(e, args);
    bool voterRegAfter = voterRegistered(voter);
    //age, voterRegAfter, voted, vote_attempts, blocked = getFullVoterDetails(voter);

    assert (!voterRegAfter => !voterRegBefore, "voter changed state from registered to not registered after a function call");
    assert (voterRegAfter => 
        ((!voterRegBefore && f.selector == registerVoter(uint8).selector) || voterRegBefore), 
            "voter was registered from an unregistered state, by other function then registerVoter()");
}

// Checks that each voted contender receieves the correct amount of points after each vote
rule correctPointsIncreaseToContenders(address first, address second, address third){
    env e;
    uint256 firstPointsBefore = getPointsOfContender(first);
    uint256 secondPointsBefore = getPointsOfContender(second);
    uint256 thirdPointsBefore = getPointsOfContender(third);

    vote(e, first, second, third);
    uint256 firstPointsAfter = getPointsOfContender(first);
    uint256 secondPointsAfter = getPointsOfContender(second);
    uint256 thirdPointsAfter = getPointsOfContender(third);
    
    assert (firstPointsAfter - firstPointsBefore == 3, "first choice receieved other amount than 3 points");
    assert (secondPointsAfter - secondPointsBefore == 2, "second choice receieved other amount than 2 points");
    assert ( thirdPointsAfter- thirdPointsBefore == 1, "third choice receieved other amount than 1 points");

}

// Checks that a blocked voter cannot get unlisted
rule onceBlockedNotOut(method f, address voter){
    env e; calldataarg args;
    // uint256 age; bool registeredBefore; bool voted; uint256 vote_attempts; bool blocked_before;
    // age, registeredBefore, voted, vote_attempts, blocked_before = getFullVoterDetails(voter);
    bool registeredBefore = voterRegistered(voter);
    bool blocked_before = blockedVoter(voter);
    require blocked_before => registeredBefore;
    f(e, args);
    // bool registeredAfter; bool blocked_after;
    // age, registeredAfter, voted, vote_attempts, blocked_after = getFullVoterDetails(voter);
    bool blocked_after = blockedVoter(voter);
    assert blocked_before => blocked_after, "the specified user got out of the blocked users' list";
}

// Checks that a contender's point count is non-decreasing
rule contendersPointsNondecreasing(method f, address contender){
    env e; calldataarg args;
    uint8 age; bool registeredBefore; uint256 pointsBefore;
    age, registeredBefore, pointsBefore = getFullContenderDetails(contender);
    require pointsBefore > 0 => registeredBefore; 
    f(e,args);
    bool registeredAfter; uint256 pointsAfter;
    age, registeredAfter, pointsAfter = getFullContenderDetails(contender);

    assert (pointsAfter >= pointsBefore);
}

