/**
		Specification file for the Certora Prover 


		To run, execute the following command in terminal/cmd:

		certoraRun Bank.sol --verify Bank:IntegrityOfDeposit.spec --solc solc7.6

		A simple rule that checks the integrity of the deposit function. 

		Understand the counter example and then rerun:

		certoraRun BankFixed.sol:Bank --verify Bank:IntegrityOfDeposit.spec --solc solc7.6

**/

rule solve() {
	// The env type represents the EVM parameters passed in every
	//   call (msg.*, tx.*, block.* variables in solidity).
	env e;
	bool solved = isSolved();
	
	
	// Verify that the funds of msg.sender is the sum of her funds before and the amount deposited.
	assert(!solved, "Solved");
}

assert(!solved, "Solved");
} 