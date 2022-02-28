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

rule MethodsVacuityCheck(method f) {
	env e; 
    calldataarg args;
	f(e, args);
	assert false, "this method should have a non reverting path";
}