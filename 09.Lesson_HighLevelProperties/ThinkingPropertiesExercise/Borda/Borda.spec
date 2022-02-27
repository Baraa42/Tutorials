
methods{
    getFullVoterDetails(address) returns (uint8, bool, bool, uint256, bool) envfree
    getFullContenderDetails(address) returns (uint8, bool, uint256) envfree
    getPointsOfContender(address) returns (uint256) envfree
    registerVoter(uint8) returns (bool)
    hasVoted(address) returns (bool) envfree
    getWinner() returns (address, uint256) envfree
    registerContender(uint8) returns (bool)
    vote(address, address, address) returns(bool)
    
}



function voterRegistered(address voter) returns bool {
    uint8 age; bool voterReg; bool voted; uint256 vote_attempts; bool blocked;
    age, voterReg, voted, vote_attempts, blocked = getFullVoterDetails(voter);
    return voterReg;   
}

function voterAttempts(address voter) returns uint256 {
    uint8 age; bool voterReg; bool voted; uint256 vote_attempts; bool blocked;
    age, voterReg, voted, vote_attempts, blocked = getFullVoterDetails(voter);
    return vote_attempts;   
}

function contenderRegistered(address contender) returns bool {
    uint8 age; bool contentedReg; uint256 points; 
    age, contentedReg, points = getFullContenderDetails(contender);
    return contentedReg;   
}

function voterBlocked(address voter) returns bool {
    uint256 age; bool voterReg; bool voted; uint256 vote_attempts; bool blocked;
    age, voterReg, voted, vote_attempts, blocked = getFullVoterDetails(voter);
    return blocked;   
}

function voterVoted(address voter) returns bool {
    uint256 age; bool voterReg; bool voted; uint256 vote_attempts; bool blocked;
    age, voterReg, voted, vote_attempts, blocked = getFullVoterDetails(voter);
    return voted;   
}

// Checks that a voter can only go from non-registered to registered only after a call to registerVoter
rule transitionToRegisteredVoter(method f, address voter){
    env e; 
    calldataarg args;

    bool voterRegBefore = voterRegistered(voter);
    f(e, args);
    bool voterRegAfter = voterRegistered(voter);

    assert (!voterRegAfter => !voterRegBefore, "voter changed state from registered to not registered after a function call");
    assert (voterRegAfter => 
        ((!voterRegBefore && f.selector == registerVoter(uint8).selector) || voterRegBefore), 
            "voter was registered from an unregistered state, by other function then registerVoter()");
}

// Checks that a contender can only go from non-registered to registered only after a call to registerContender
rule transitionToRegisteredContender(method f, address contender){
    env e; 
    calldataarg args;

    bool regBefore = contenderRegistered(contender);
    f(e, args);
    bool regAfter = contenderRegistered(contender);

    assert (!regAfter => !regBefore, "voter changed state from registered to not registered after a function call");
    assert (regAfter => 
        ((!regBefore && f.selector == registerContender(uint8).selector) || regBefore), 
            "voter was registered from an unregistered state, by other function then registerContender()");
}

// Checks that a voter can not vote more than once
rule cannotVoteMoreThanOnce(method f, address voter){
    env e; 
    calldataarg args;

    bool votedBefore = voterVoted(voter);
    bool vote_success = vote(e, args);

    

    assert (e.msg.sender == voter && votedBefore) => !vote_success, "Voted more than once";
  
}

// Checks that a blocked voter cannot get unlisted
rule onceBlockedNotOut(method f, address voter){
    env e; 
    calldataarg args;

    bool registeredBefore = voterRegistered(voter);
    bool blocked_before = voterBlocked(voter);

    require blocked_before => registeredBefore;
    f(e, args);
    bool blocked_after = voterBlocked(voter);

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
