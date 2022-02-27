# Properties For Borda

First, let us define the states of the system:

```ruby
- `defContenderNonRegistered` - (Contender Non-Registered) is defined as `_contender[contender].registered` is 0.
- `defContenderRegistered` - (Contender Registered) is defined as `_contender[contender].registered` is 1.
- `defVoterNonRegistered` - (Voter Non-Registered) is defined as `_voters[voter].registered` is 0.
- `defVoteRegisteredNotVotedNonBlack` - (Voter Registered Not Black Listed ) is defined as `_voters[voter].registered` is 1 and `_voters[voter].black_listed` is 0 and `_voters[voter].voted` is 0.
- `defVoteRegisteredVotedNonBlack` - (Voter Registered Not Black Listed ) is defined as `_voters[voter].registered` is 1 and `_voters[voter].black_listed` is 0 and `_voters[voter].voted` is 1.

- `defVoteRegisteredBlack` - (Voter Registered Black Listed ) is defined as `_voters[voter].registered` is 1 and `_voters[voter].black_listed` is 1.

```

1. ***Valid state*** - `defContenderNonRegistered` => `_contender[contender].registered` == 0 && `_contender[contender].age` == 0 && `_contender[contender].points` == 0 .
2. ***Valid state*** - `defContenderRegistered` => `_contender[contender].registered` == 1.
3. ***Valid state*** - `defVoterNonRegistered` => `_voters[voter].registered`  == 0 && `_voters[voter].age` == 0 && `_voters[voter].voted` == 0 .

...........


4. ***State transitions*** - The only allowed state transitions are : 
    - `defContenderNonRegistered` to `defContenderRegistered` only after a call to `registerContender()`.
    - `defVoterNonRegistered` to `defVoteRegisteredNotVotedNonBlack` only after a call to `registerVoter()`.
    - `defVoteRegisteredNotVotedNonBlack` to `defVoteRegisteredVotedNonBlack` only after a call to `vote()`.
    - `defVoteRegisteredVotedNonBlack` to `defVoteRegisteredVotedBlack` only after a call to `vote()`.


7. ***Variable transition*** - `_contender[contender].registered` and cannot be changed if state is not `defContenderNonRegistered`.
8. ***Variable transition*** - `_voters[voter].registered` and cannot be changed if state is not `defVoteRegisteredNotVotedNonBlack`.
..........


9. ***High-level*** - No way to vote more than once. 
10. ***High-level*** - No way to vote if blacklisted. 
11. ***High-level*** - No way to decrease a contender points. 



12. ***Unit tests***  : 
    - `registerContender()` correctly changes state of `_contenders[msg.sender]` if state is `defContenderNonRegistered`.
    - `registerVoter()` correctly changes state of `_voters[msg.sender]` if state is `defVoterNonRegistered`.
    .......
    

    


</br>

---

## Prioritizing

</br>



### High Priority:

- Properties 1 to 4 are high priority because if they fail, the idea of the system fails.
- Properties 7 and 8 are high priority because if they fail a voter/contender can fail to have his right to register.
- Properties 9 and 11 is high priority because if they are essential to the system correct function, the rules described must be followed.


### Low Priority:

- Properties 11 is low priority since:
    1. They check implementation of a specific function (as oppose to multiple functions).
    2. They fairly simple to check by other means, including by manual reviewing of the code.