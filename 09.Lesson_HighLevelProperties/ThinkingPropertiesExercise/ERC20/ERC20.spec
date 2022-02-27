methods {
	
    totalSupply() returns (uint256) envfree
    balanceOf(address) returns (uint256) envfree
    transfer(address, uint256) returns (bool)
    transferFrom(address,address, uint256) returns (bool)
    allowance(address , address)  returns (uint256) envfree
    approve(address , uint256 )  returns (bool) 
    
}

// total funds greater than single account balance
invariant totalFunds_GE_single_user_funds()
    forall address user. totalSupply() >= balanceOf(user)


ghost sum_of_all_funds() returns uint256{
    // for the constructor - assuming that on the constructor the value of the ghost is 0
    init_state axiom sum_of_all_funds() == 0;
}

hook Sstore _balances[KEY address user] uint256 new_balance
    // the old value ↓ already there
    (uint256 old_balance) STORAGE {
  
  havoc sum_of_all_funds assuming sum_of_all_funds@new() == sum_of_all_funds@old() + new_balance - old_balance;
}

invariant totalFunds_GE_to_sum_of_all_funds()
    totalSupply() >= sum_of_all_funds()





rule transferReturn(address user, uint256 amount) {
    env e;

    uint256 balance = balanceOf(e.msg.sender);
    bool transfer_return = transfer(e,user, amount);

    assert balance < amount => !transfer_return;

}

rule transferFromReturn(address sender, address recipient, uint256 amount) {
    env e;

    uint256 balance = balanceOf(sender);
    uint256 allowance = allowance(sender, e.msg.sender);
    bool transfer_return = transferFrom(e,sender, recipient, amount);

    assert ((balance < amount) || (allowance < amount) ) => !transfer_return;

}

rule balancePreservation(address user,uint256 amount, method f) {
    env e;
    calldataarg args;

    uint256 balanceBefore = balanceOf(user);
    uint256 allowance = allowance(user, e.msg.sender);
    f(e, args);
    uint256 balanceAfter = balanceOf(user);

    assert  balanceBefore > balanceAfter => ((e.msg.sender == user) || allowance > 0);

}






// rule IntegrityOfDepositForUser(address user) {
//     env e;
//     calldataarg args;
//     uint256 totalBefore = balanceOf(user);
//     deposit(e);
//     require e.msg.sender == user;
//     uint256 totalAfter = balanceOf(user);
//     assert totalAfter == totalBefore + e.msg.value, "TotalFees decreased";
// }

// rule IntegrityOfWithdraw(uint256 amount) {
//     env e;
//     calldataarg args;
//     uint256 totalBefore = totalSupply();
//     withdraw(e, amount);
//     uint256 totalAfter = totalSupply();
//     assert totalAfter == totalBefore - amount, "TotalFees decreased";
// }

// rule IntegrityOfWithdrawForUser(address user, uint256 amount) {
//     env e;
//     calldataarg args;
//     uint256 totalBefore = balanceOf(user);
//     withdraw(e, amount);
//     require e.msg.sender == user;
//     uint256 totalAfter = balanceOf(user);
//     assert totalAfter == totalBefore - amount, "TotalFees decreased";
// }