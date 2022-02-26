methods {
	getCurrentManager(uint256 fundId) returns (address) envfree
	getPendingManager(uint256 fundId) returns (address) envfree
	isActiveManager(address a) returns (bool) envfree
}

rule uniqueManager(uint256 fundId1, uint256 fundId2, method f) {
	require fundId1 != fundId2;
	require getCurrentManager(fundId1) != 0 => isActiveManager(getCurrentManager(fundId1)); // manager1 != 0 && isActiveManager(manager1)
	require getCurrentManager(fundId2) != 0 => isActiveManager(getCurrentManager(fundId2)); // manager2 != 0 && isActiveManager(manager2)
	require getCurrentManager(fundId1) != getCurrentManager(fundId2);                       // manager1 != manager2
				
	env e;
	if (f.selector == claimManagement(uint256).selector)
	{
		uint256 id;
		require id == fundId1 || id == fundId2;
		claimManagement(e, id);  
	}
	else {
		calldataarg args;
		f(e,args);
	}
	assert getCurrentManager(fundId1) != getCurrentManager(fundId2), "managers not different";
	assert getCurrentManager(fundId1) != 0 => isActiveManager(getCurrentManager(fundId1)), "manager of fund1 is not active";
	assert getCurrentManager(fundId2) != 0 => isActiveManager(getCurrentManager(fundId2)), "manager of fund2 is not active";
}

// rule uniqueManagerAsRule(uint256 fundId1, uint256 fundId2, method f) {
// 	// assume different IDs
// 	require fundId1 != fundId2;
// 	// assume different managers
// 	address manager1 = getCurrentManager(fundId1);
// 	address manager2 = getCurrentManager(fundId2);
// 	require manager1 != manager2;
// 	// hint: add additional variables just to look at the current state
// 	bool active1 = isActiveManager(manager1);
// 	bool active2 = isActiveManager(manager2);			
// 	require manager1 != 0 => active1;
// 	require manager2 != 0 => active2;
// 	env e;
// 	calldataarg args;
// 	f(e,args);

// 	address manager1After = getCurrentManager(fundId1);
// 	address manager2After = getCurrentManager(fundId2);
// 	// bool active1After = isActiveManager(manager1After);
// 	// bool active2After = isActiveManager(manager2After);
// 	// assert manager1After != 0 => active1After;
// 	// assert manager2After != 0 => active2After;

// 	// verify that the managers are still different 
// 	assert manager1After != manager2After, "managers not different";
// }


// /* A version of uniqueManagerAsRule as an invariant */
// invariant uniqueManagerAsInvariant(uint256 fundId1, uint256 fundId2)
	// ((fundId1 != fundId2) && (getCurrentManager(fundId1) != 0 || getCurrentManager(fundId2) != 0) ) => getCurrentManager(fundId1) != getCurrentManager(fundId2) 
