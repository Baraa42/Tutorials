methods {
	
	getTokenAtIndex(uint256) returns(address) envfree
	getIdOfToken(address) returns(uint256) envfree
	getReserveCount() returns(uint256) envfree
	addReserve(address, address, address, uint256) envfree
	removeReserve(address) envfree
}


// proving correlation
invariant correlation(uint256 tokenId)
         
		getTokenAtIndex(tokenId) != 0 => getIdOfToken(getTokenAtIndex(tokenId)) == tokenId
	{
		preserved addReserve(address token, address stableToken, address varToken, uint256 fee) {
			require token != 0;
			bool alreadyAdded = getTokenAtIndex(getIdOfToken(token)) != 0 || getTokenAtIndex(0) == token;
			require !alreadyAdded;
		}
		
		preserved removeReserve(address token) {
			require getTokenAtIndex(getIdOfToken(token)) != 0;
		}
	}

// proving correlation of List
invariant correlationOfLists(address _token)
		(getIdOfToken(_token) != 0 || (getIdOfToken(_token) == 0 && getTokenAtIndex(0) == _token) ) => getTokenAtIndex(getIdOfToken(_token)) == _token
	{
		preserved addReserve(address token, address stableToken, address varToken, uint256 fee) {
			require token != 0;
			bool alreadyAdded = getTokenAtIndex(getIdOfToken(token)) != 0 || getTokenAtIndex(0) == token;
			require !alreadyAdded;
		}
		
		preserved removeReserve(address token) {
			require getTokenAtIndex(getIdOfToken(token)) != 0;
            requireInvariant injectivityOfTokens(token, _token);
		}
	}

// proving injectivity
invariant injectivity(uint tokenId1, uint tokenId2, address token1, address token2)
        
		(token1 == getTokenAtIndex(tokenId1) && token2 == getTokenAtIndex(tokenId2) && token1 != token2) => tokenId1 != tokenId2
	{
		preserved addReserve(address token, address stableToken, address varToken, uint256 fee) {
			require token != 0;
			bool alreadyAdded = getTokenAtIndex(getIdOfToken(token)) != 0 || getTokenAtIndex(0) == token;
			require !alreadyAdded;
		}
		
		preserved removeReserve(address token) {
			require getTokenAtIndex(getIdOfToken(token)) != 0;
		}
	}

// proving injectivity of Tokens
invariant injectivityOfTokens(address token1, address token2)
        (token1 != token2 && getIdOfToken(token1) != 0)  => (getIdOfToken(token1) != getIdOfToken(token2))
	{
		preserved addReserve(address token, address stableToken, address varToken, uint256 fee) {
			require token != 0;
			bool alreadyAdded = getTokenAtIndex(getIdOfToken(token)) != 0 || getTokenAtIndex(0) == token;
			require !alreadyAdded;
		}
		
		preserved removeReserve(address token) {
			require getTokenAtIndex(getIdOfToken(token)) != 0;
		}
	}

// independency of tokens
rule independencyOfTokensInAList(address token1, address token2, address stableToken, address varToken, uint256 fee, method f) {
	env e;
	require token1 != token2;
    // requireInvariant injectivityOfTokens(token1, token2);
    // requireInvariant correlationOfLists(token1, token2);
	uint256 tokenId1Before = getIdOfToken(token1);
    uint256 tokenId2Before = getIdOfToken(token2);
     
    
	
	if (f.selector == addReserve(address, address, address, uint256).selector)
		{
		
        require token2 != 0;
		bool alreadyAdded = getTokenAtIndex(getIdOfToken(token2)) != 0 || getTokenAtIndex(0) == token2;
		require !alreadyAdded;
		addReserve(token2, stableToken, varToken, fee);
	}
	else {
        require getTokenAtIndex(getIdOfToken(token2)) != 0;
		removeReserve(token2);
	}
	
	uint256 tokenId1After = getIdOfToken(token1);
	assert tokenId1Before == tokenId1After, "not same Id after function call";
	
}

// independency of tokens
rule independencyOfTokensInAList1(address token1, address token2, address stableToken, address varToken, uint256 fee) {
	env e;
	require token1 != token2;
    requireInvariant injectivityOfTokens(token1, token2);
    requireInvariant correlationOfLists(token1); 
    requireInvariant correlationOfLists(token2);
    //require getTokenAtIndex(getIdOfToken(token2)) != 0;
	uint256 tokenId1Before = getIdOfToken(token1);
    removeReserve(token2);
    uint256 tokenId1After = getIdOfToken(token1);
    assert tokenId1Before == tokenId1After, "not same Id after function call";

	
}

// increase/decrease in reserve count
rule addRemoveChangeReserveCountBy1(address token, address stableToken, address varToken, uint256 fee, method f) {
    env e;

    uint256 reserveBefore = getReserveCount();

    if (f.selector == addReserve(address, address, address, uint256).selector)
		{
		
        require token != 0;
		bool alreadyAdded = getTokenAtIndex(getIdOfToken(token)) != 0 || getTokenAtIndex(0) == token;
		require !alreadyAdded;

		addReserve(token, stableToken, varToken, fee);
	}
	else {
        require getTokenAtIndex(getIdOfToken(token)) != 0;
		removeReserve(token);

	}

    uint256 reserveAfter = getReserveCount();
    assert reserveAfter - reserveBefore == 1 || reserveAfter - reserveBefore == -1, "wrong increase/decrease in reserveCount";

}



