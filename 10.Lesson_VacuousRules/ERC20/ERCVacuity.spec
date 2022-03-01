methods{
    totalSupply() returns (uint256) envfree
    balanceOf(address) returns (uint256) envfree
    transfer(address, uint256) returns (bool)
    allowance(address, address) returns (uint256) envfree
    increaseAllowance(address, uint256) returns (bool)
    decreaseAllowance(address, uint256) returns (bool)
    approve(address, uint256) returns (bool)
    transferFrom(address, address, uint256) returns (bool)
    mint(address, uint256)
    burn(address, uint256)
}    

// sum of 2 accounts' balances cannot be less than a single one of them
// run without --rule_sanity is green
// run with --rule_sanity is red
invariant twoBalancesGreaterThanSingle(address account1, address account2)
    balanceOf(account1) + balanceOf(account2) < balanceOf(account1) => false // tautology false => false

// common mistake - not before and after
// run without --rule_sanity is green
// run with --rule_sanity is red
invariant twoBalancesGreaterThanSingleProb(address account1, address account2)
    balanceOf(account1) + balanceOf(account2) <= balanceOf(account1) + balanceOf(account2) // tautology always true


// totalSupply & user's balance ratios
// run without --rule_sanity is green
// run with --rule_sanity is red
invariant balanceRatios(address account1, address account2)
    totalSupply() == balanceOf(account1) + balanceOf(account2) =>
        (( balanceOf(account1) + balanceOf(account2) == 0 ) =>
            totalSupply() + balanceOf(account1) >= balanceOf(account2) ) // tautology alwas true

/* 
 * Try to think about how we can check if this rule is a tautology.
 * It is not as simple as copying the assert to a rule.
 * These problems are being addressed by the Certora team as we try to automate checks for vacuity.
 */
// checks the integrity of increaseAllowance
// run without --rule_sanity is green
// run with --rule_sanity is green
// rule is fine
rule increaseAllowanceIntegrity(address spender, uint256 amount){
    env e;
    address owner;
    require owner == e.msg.sender;
    uint256 _allowance = allowance(owner, spender);
    increaseAllowance(e, spender, amount);
    uint256 allowance_ = allowance(owner, spender);
    assert _allowance <= allowance_;
}

// Checks if the correctness of power balance between 2 users is kept.
// run without --rule_sanity is green
// run with --rule_sanity is red
// rule is not sane
rule transferOutDoesNotChangePowerBalance(address user1, address user2, address user3, uint256 amount){
    env e; calldataarg args;
    uint256 _balance1; uint256 _balance2;
    require _balance1 == balanceOf(user1);
    require e.msg.sender == user1;
    // require _balance2 == balanceOf(user1); // problem here should be user2
    require _balance2 == balanceOf(user2);
    require _balance1 < _balance2;
    
    transfer(e, user3, amount);

    uint256 balance1_ = balanceOf(user1);
    uint256 balance2_ = balanceOf(user2);

    assert balance1_ < balance2_;
}

/* Hint: 
 * lastReverted stores information on the last function call only
*/
// run without --rule_sanity is green
// run with --rule_sanity is green
// rule is fine
rule lastRevertedExample(address sender, address recipient, uint256 amount){
    env e;
    uint256 _allowance = allowance(sender, recipient);
    transferFrom@withrevert(e, sender, recipient, amount);
    uint256 allowance_ = allowance(sender, recipient);

    assert lastReverted => _allowance < amount;
}

// run without --rule_sanity is green
// run with --rule_sanity is red
// rule is not sane
rule ownerChange(address currentOwner, address user){
    env e; calldataarg args; method f;
    address ownerBefore = _owner(e);
    require currentOwner == ownerBefore && user != currentOwner;
    f(e, args);
    address ownerAfter = _owner(e);
    assert ownerAfter != currentOwner || ownerAfter != user; // this assert is always true, there is no reverting path that would lead to it being false since user != currentOwner
}

// checks that each function changes balance of at most one user
// run without --rule_sanity is green
// run with --rule_sanity is red
// rule is not sane
rule balanceOfChange(method f, address user1, address user2) {
    uint256 balanceOf1Before = balanceOf(user1);
    uint256 balanceOf2Before = balanceOf(user2);
    require !((!(balanceOf1Before < balanceOf2Before)) && (!(balanceOf2Before < balanceOf1Before))); // require b1 < b2 && b2 >= b1 basicaly b1 < b2
    env e;
    calldataarg args;
    f(e, args);
    uint256 balanceOf1After = balanceOf(user1);
    uint256 balanceOf2After = balanceOf(user2);
    assert ((balanceOf1After != balanceOf1Before) &&   // assert (b1after != b1before) && (b2after != b2before)  => user1 != user2
            (balanceOf2After != balanceOf1Before))     // we already require user1 != user2 so this implication is always true regardless of the path taken
               => user1 != user2; 
}

// checks that mint and burn are inverse operations
// run without --rule_sanity is green
// run with --rule_sanity is green
// rule is fine
rule mintBurnInverse(address user, uint256 amount) {
    uint256 balanceBefore = balanceOf(user);
    env e;
    mint(e, user, amount);
    burn(e, user, amount);
    uint256 balanceAfter = balanceOf(user);
    assert balanceBefore == balanceAfter;
}

// now going back to Spartan and Popsicle ...
// After running with --rule_sanity :
/*        RESULTS
- Popsicle :
    --Sum Of All users Didnt pass
    -- No reverting path which is by design
    -- totalFeesEarnedPerShareIncreasing also failed which is normal since there is no function in the code that reduce it