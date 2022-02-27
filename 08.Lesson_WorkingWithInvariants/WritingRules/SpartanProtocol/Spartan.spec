methods {
	
	init_pool() 
	add_liquidity() returns (uint256) 
    remove_liquidity(uint) 
	swap(address) 
	getToken0DepositAddress() returns (address) envfree
    getToken1DepositAddress() returns (address) envfree
    getToken0Amount() returns (uint) envfree
    getToken1Amount() returns (uint) envfree
    getK() returns (uint) envfree
    getInit() returns (bool) envfree
    
    sync() envfree

    totalSupply() returns (uint256) envfree
    balanceOf(address) returns (uint256) envfree
    transfer(address, uint256) returns (bool)
    transferFrom(address,address, uint256) returns (bool)
    getAllowance(address , address)  returns (uint256) envfree
    approve(address , uint256 )  returns (bool) 
    increase_allowance(address , uint ) 
    decrease_allowance(address , uint ) 

    
}



// invariant totalFeesEarnedPerShare_GE_feesCollectedPerShare_single_user()
//     // A quantifier is followed by a declaration of a variable to say "for all users, $exp$ should hold"
//     // Quantifiers are raising the complexity of of the run by a considerable amount, so often using them will result in a timeout
//     forall address user. getTotalFeesEarnedPerShare() >= getFeesCollectedPerShare(user)


invariant supply_GE_single_user_balance(address user)
        totalSupply() >= balanceOf(user)
		
	{
		preserved transfer(address recipient, uint256 amount) with (env e1)  {
			require e1.msg.sender == user || totalSupply() >= balanceOf(user) + balanceOf(e1.msg.sender) ;
			
		}
		
		preserved transferFrom(address sender, address recipient, uint256 amount) with (env e2) {
			require sender == recipient || totalSupply() >= balanceOf(sender) + balanceOf(recipient);
		}

        preserved init_pool()  with (env e3) {
			require !getInit();
		}

	}


rule tokenAmountIncreaseSameTime(method f) {
    env e;
    calldataarg args;

    uint256 token0before = getToken0Amount();
    uint256 token1before = getToken1Amount();
    f(e, args);
    uint256 token0After = getToken0Amount();
    uint256 token1After = getToken1Amount();

    assert ((token1After > token1before) && (token0After > token0before)) => (f.selector == add_liquidity().selector) || (f.selector == init_pool().selector), "Wrong amount mouvement";
    
}

rule tokenAmountDecreaseSameTime(method f) {
    env e;
    calldataarg args;

    uint256 token0before = getToken0Amount();
    uint256 token1before = getToken1Amount();
    f(e, args);
    uint256 token0After = getToken0Amount();
    uint256 token1After = getToken1Amount();

    assert (token1After < token1before) && (token0After < token0before) => f.selector == remove_liquidity(uint).selector, "Wrong amount mouvement";
    
}

rule tokenAmountsOppositeDirections(method f) {
    env e;
    calldataarg args;

    uint256 token0before = getToken0Amount();
    uint256 token1before = getToken1Amount();
    f(e, args);
    uint256 token0After = getToken0Amount();
    uint256 token1After = getToken1Amount();

    bool b0 = token0After < token0before;
    bool b1 = token1After > token1before;
   
    assert (b0 && b1) || (!b0 && !b1) => f.selector == swap(address).selector, "Wrong amount mouvement";
    
}

rule KConstantAfterSwap(method f) {
    env e;
    calldataarg args;
    
    uint256 KBefore = getK();
    swap(e, args);
    uint256 KAfter = getK();

    assert KAfter == KBefore, "K shouldnt change after a swap";

}

// rule totalFeesEarnedPerShareIncreasing(method f) {
//     env e;
//     calldataarg args;
//     uint256 totalBefore = getTotalFeesEarnedPerShare();
//     f(e, args);
//     uint256 totalAfter = getTotalFeesEarnedPerShare();
//     assert totalAfter >= totalBefore, "TotalFees decreased";
    
// }

// rule IntegrityOfDepositForTotalSupply() {
//     env e;
//     calldataarg args;
//     uint256 totalBefore = totalSupply();
//     deposit(e);
//     uint256 totalAfter = totalSupply();
//     assert totalAfter == totalBefore + e.msg.value, "TotalFees decreased";
// }


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