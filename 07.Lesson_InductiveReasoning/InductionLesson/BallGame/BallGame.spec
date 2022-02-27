
methods {
	ballAt() returns uint256 envfree
}

invariant neverReachPlayer4() 
	ballAt() != 4 && ballAt() != 3

rule neverToPlayer4(method f) {
	env e;
	calldataarg args;
	uint256 ballBefore = ballAt();
	require ballBefore != 4 && ballBefore != 3;
	f(e, args);
	uint256 ballAfter = ballAt();
	assert ballAfter != 4 && ballAfter != 3;
}