## Properties Solution

- For each user e : totalSupply() >= balances(e)
- If totalSupply() increase then the f.selector == close
- After a call to any function totalSupply() is non-decreasing.
- After a call to transferTo : totalSupply() doesn't change.
- After a call to transferTo : oldBalance(sender) + oldBalance(receiver) = newBalance(sender) + newBalance(receiver)
- auctions[id].end_time == 0 => There was never an auction with `id` or there were auctions with `id` that were closed : bad design in my opinion
- auctions[id].prize == 2**256-1 => No bid yet after creation
- prize = getPrizeById(id) is non-increasing after a function call.
- winner = getAuctionWinner(id) can only change after function call if function is : bid or close or newAuction 

