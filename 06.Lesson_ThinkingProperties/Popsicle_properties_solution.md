# Properties For Auction


1. ***Valid state*** - `owner()` is not 0.

2. ***Valid state*** - `accounts(e).feesCollectedPerShare` <= `totalFeesEarnedPerShare()`>.

3. ***Variable transition*** - `owner()` can never be changed.

4. ***Variable transition*** - `totalFeesEarnedPerShare()` can is non-decreasing and can only be changed after a call to `OwnerDoItsJobAndEarnsFeesToItsClients()`.

5. ***Variable transition*** - `accounts(e).feesCollectedPerShare` is non-decreasing and can only be changed after a call to `deposit()` or `collectFees()`.

6. ***High-level*** - No way to change `owner()`. 

7. ***High-level*** - No way to decrease `totalFeesEarnedPerShare()`. 

8. ***High-level*** - Solvency - Total ether in contract is greater or equal to the sum of `assetsOf()` of all users. The system has enough `Eth` to pay everyone what the deserve.

9. ***Unit tests*** - deposit() correctly changes `balances[who]` and `accounts[who]` and `totalSupply`.

10. ***Unit tests*** - withdraw() correctly changes `balances[who]` and `accounts[who]` and `totalSupply`.

11. ***Unit tests*** - collectFees() correctly changes `balances[who]` and `accounts[who]` and `totalSupply`.

</br>

---

## Prioritizing

</br>


### High Priority:

- Property 1 is high priority because owner can increase `totalFeesEarnedPerShare` and if's 0 then system can't function as intended.

- Properties 2 and 5 are high priority because if they fail the user can't withdraw the funds he is rightly owed.

- Property 3 and 4, 6 are high priority because owner can increase `totalFeesEarnedPerShare` which if used inappropriately can cause theft of funds.

- Property 3 is high priority because `mint()` increases a value of `totalSupply` that can block other auctions to finish if you can claim huge prize. Also we want to prevent attacker from getting additional benefits.

- Properties 7 is high priority because violation of this rule means that attacker can unjustly withdraw more than he is owed.

- Property 8 is high priority because we want to system to be solvent at any moment to pay uses their funds.



### Low Priority:

- Properties 9 to 11 are low priority since:
    1. They check implementation of a specific function (as oppose to multiple functions).
    2. They fairly simple to check by other means, including by manual reviewing of the code.