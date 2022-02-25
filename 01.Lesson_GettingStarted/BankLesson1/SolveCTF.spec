/**
		Specification file for the Certora Prover 


		To run, execute the following command in terminal/cmd:

		certoraRun Bank.sol --verify Bank:IntegrityOfDeposit.spec --solc solc7.6

		A simple rule that checks the integrity of the deposit function. 

		Understand the counter example and then rerun:

		certoraRun BankFixed.sol:Bank --verify Bank:IntegrityOfDeposit.spec --solc solc7.6

**/

rule solve(uint32 seed) {
	// The env type represents the EVM parameters passed in every
	//   call (msg.*, tx.*, block.* variables in solidity).
	env e;
	uint16 solution = roll(e, seed);
	
	
	// Verify that the funds of msg.sender is the sum of her funds before and the amount deposited.
	assert(solution != 1073741824 && solution != 2147483648 && solution != 3221225472  );
}

} 