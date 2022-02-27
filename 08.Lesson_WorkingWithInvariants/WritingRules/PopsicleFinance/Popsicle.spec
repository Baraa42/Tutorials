methods {
	
	deposit() 
	withdraw(uint256) 
    collectFees() 
	OwnerDoItsJobAndEarnsFeesToItsClients() 
	assetsOf(address) returns (uint256) envfree

    totalSupply() returns (uint256) envfree
    balanceOf(address) returns (uint256) envfree
    transfer(address, uint256) returns (bool)
    transferFrom(address,address, uint256) returns (bool)
    allowanceOf(address , address )  returns (uint256) envfree
    approve(address , uint256 )  returns (bool) 
    increase_allowance(address , uint ) 
    decrease_allowance(address , uint ) 

    getTotalFeesEarnedPerShare() returns (uint256) envfree
    getFeesCollectedPerShare(address) returns (uint256) envfree
    contractBalance() returns (uint256) envfree

    
}

// 1. totalFeesEarnedPerShare >= feesCollectedPerShare -- Need getters for this
// 2. totalFeesEarnedPerShare non-decreasing
// 3. total Ether in contract >= assetsOf(user)
// 4. deposit increase total supply ok
// 5. withdraw decrease total supply ok

// Step :
// 3. Write invariants for the sum for all users
// 4. Copy already made code 

invariant totalFunds_GE_single_user_funds()
    // A quantifier is followed by a declaration of a variable to say "for all users, $exp$ should hold"
    // Quantifiers are raising the complexity of of the run by a considerable amount, so often using them will result in a timeout
    forall address user. totalSupply() >= balanceOf(user)

/* A declaration of a ghost.
 * A ghost is, in esssence, an uninterpeted function (remember lesson 3?).
 * This ghost takes no arguments and returns a type mathint.
 */
ghost sum_of_all_funds() returns uint256{
    // for the constructor - assuming that on the constructor the value of the ghost is 0
    init_state axiom sum_of_all_funds() == 0;
}

hook Sstore balances[KEY address user] uint256 new_balance
    // the old value ↓ already there
    (uint256 old_balance) STORAGE {
  
  havoc sum_of_all_funds assuming sum_of_all_funds@new() == sum_of_all_funds@old() + new_balance - old_balance;
}

invariant totalFunds_GE_to_sum_of_all_funds()
    totalSupply() >= sum_of_all_funds()


// rule can_withdraw() {
//     env e;

//     uint256 balance_before = getEthBalance(e.msg.sender);
//     uint256 reserves       = getEthBalance(currentContract);
//     uint256 funds_before   = getFunds(e.msg.sender);

//     withdraw@withrevert(e);

//     uint256 balance_after  = getEthBalance(e.msg.sender);
//     assert balance_after == balance_before + funds_before;
// }



// proving totalSupply greater than user balance
invariant supply_GE_single_user_balance(address user)
        totalSupply() >= balanceOf(user)
		
	{
		preserved transfer(address recipient, uint256 amount) with (env e1)  {
			require e1.msg.sender == user || totalSupply() >= balanceOf(user) + balanceOf(e1.msg.sender) ;
			
		}
		
		preserved transferFrom(address sender, address recipient, uint256 amount) with (env e2) {
			require sender == recipient || totalSupply() >= balanceOf(sender) + balanceOf(recipient);
		}

        preserved withdraw(uint256 amount) with (env e3) {
			require  amount <= balanceOf(e3.msg.sender) && e3.msg.sender != user => totalSupply() >= balanceOf(user) + balanceOf(e3.msg.sender)  ;
		}
	}

rule totalFeesEarnedPerShareIncreasing(method f) {
    env e;
    calldataarg args;
    uint256 totalBefore = getTotalFeesEarnedPerShare();
    f(e, args);
    uint256 totalAfter = getTotalFeesEarnedPerShare();
    assert totalAfter >= totalBefore, "TotalFees decreased";
    
}

rule IntegrityOfDepositForTotalSupply() {
    env e;
    calldataarg args;
    uint256 totalBefore = totalSupply();
    deposit(e);
    uint256 totalAfter = totalSupply();
    assert totalAfter == totalBefore + e.msg.value, "TotalFees decreased";
}


rule IntegrityOfDepositForUser(address user) {
    env e;
    calldataarg args;
    uint256 totalBefore = balanceOf(user);
    deposit(e);
    require e.msg.sender == user;
    uint256 totalAfter = balanceOf(user);
    assert totalAfter == totalBefore + e.msg.value, "TotalFees decreased";
}

rule IntegrityOfWithdraw(uint256 amount) {
    env e;
    calldataarg args;
    uint256 totalBefore = totalSupply();
    withdraw(e, amount);
    uint256 totalAfter = totalSupply();
    assert totalAfter == totalBefore - amount, "TotalFees decreased";
}

rule IntegrityOfWithdrawForUser(address user, uint256 amount) {
    env e;
    calldataarg args;
    uint256 totalBefore = balanceOf(user);
    withdraw(e, amount);
    require e.msg.sender == user;
    uint256 totalAfter = balanceOf(user);
    assert totalAfter == totalBefore - amount, "TotalFees decreased";
}