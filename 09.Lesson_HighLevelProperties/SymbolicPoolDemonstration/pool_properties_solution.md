# Properties For Pool


1. ***Valid state*** - `totalSupply` >= `balanceOf(user)` for all users.
2. ***Valid state*** - `totalSupply` >= `sumUsersBalances`.

3. ***State transitions*** - `transfer(to, amount)` return true iff `balanceOf[msg.sender]` >= amount. 
4. ***State transitions*** - `transferFrom(sender, recipient, amount)` return true iff `balanceOf[sender]` >= `amount ` && `allowance[sender, msg.sender]` >= `amount`.
5. ***State transitions*** - `totalSupply` increase only after a call to deposit.
6. ***State transitions*** - `totalSupply` decrease only after a call to withdraw.
7. ***State transitions*** - `asset.balanceOf[contract]` does not decrease after a call to flashloan.


5. ***High-level*** - Solvency : `TotalSupply` >= `sumUsersBalances`. The system can pay everyone.
6. ***High-level*** - No way to decrease balance of user by someone other than the user who is not allowed.
7.  ***High-level*** - Any user can transfer up to his balance anytime.


8. ***Unit tests***  : 
- `transfer` correctly changes state of balances.
- `transferFrom` correctly changes state of balances and allowances.
- `approve` correctly changes state of allowances.
- `deposit` correctly changes asset balance of contract and `balanceOf[msg.sender]` and `totalSupply`.
- `withdraw` correctly changes asset balance of contract and `balanceOf[msg.sender]` and `totalSupply`.
    
# Properties Added For Pool after review
9. ***Valid state*** - `totalSupply` == 0 iff  `asset.balanceOf(contract)` == 0.
10. ***High-level*** -  `TotalSupply` <= `asset.balanceOf(contract)`. For each quantity `X` of asset deposited the amount of tokens minted should be less than `X`.
11. ***High-level*** -  Solvency : The contract balance `asset.balanceOf(contract)` should be greater than the sum of `sharesToAmount(user)` for all users, meaning at any point in time users can withdraw what they are owed.




</br>

---

## Prioritizing

</br>



### High Priority:

- Property 1 to 7 are high priority because if they fail, the idea of the system fails.


### Low Priority:


- Property 8 is low priority since:
    1. They check implementation of a specific function (as oppose to multiple functions).
    2. They fairly simple to check by other means, including by manual reviewing of the code.



## Prioritizing Update

### High Priority:
- Property 4 is high priority since amount of LP tokens and contract balance of asset should be correlated, in a sense that the contract `totalSupply` is a function of `asset.balanceOf(contract)` that satisfies `f(0)=0`.
- Property 11 is also high priority, every user deserve to be paid his rightful amount in `asset` and the deposit function states that 