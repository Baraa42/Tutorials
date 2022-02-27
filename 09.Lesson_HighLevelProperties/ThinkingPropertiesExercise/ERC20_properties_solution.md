# Properties For ERC20



1. ***Valid state*** - `totalSupply` >= `balanceOf(user)` for all users.
2. ***Valid state*** - `totalSupply` >= `sumUsersBalances`.


3. ***State transitions*** - `transfer(to, amount)` return true iff `balanceOf[msg.sender]` >= amount. 
4. ***State transitions*** - `transferFrom(sender, recipient, amount)` return true iff `balanceOf[sender]` >= `amount ` && `allowance[sender, msg.sender]` >= `amount`.

5. ***High-level*** - Solvency : `TotalSupply` >= `sumUsersBalances`. The system can pay everyone.
6. ***High-level*** - No way to decrease balance of user by someone other than the user who is not allowed.
7.  ***High-level*** - Any user can transfer use up to his balance anytime.


8. ***Unit tests***  : 
- `transfer` correctly changes state of balances.
- `transferFrom` correctly changes state of balances and allowances.
- `approve` correctly changes state of allowances.
    


</br>

---

## Prioritizing

</br>



### High Priority:

- Properties 1 to 7 are high priority because if they fail, the idea of the system fails.


### Low Priority:


- Properties 8 is low priority since:
    1. They check implementation of a specific function (as oppose to multiple functions).
    2. They fairly simple to check by other means, including by manual reviewing of the code.