# Properties For MeetingScheduler

First, let us define the states of the system:

```ruby
- `defEventNonCreated` - (Non created) is defined as `eventsMap[id].owner` is 0.
- `defEventCreated` - (Created) is defined as `eventsMap[id].owner` is not 0.
- `defOfferingNotAvailable` - (Non created/ deleted) is defined as `offerings[id].deadline` is 0.
- `defOfferingAvailable` - (Created) is defined as `offerings[id].deadline` is not 0.
```

1. ***Valid state*** - `defEventNonCreated` => `eventsMap[id].owner` == `eventsMap[id].ticketPrice` == `eventsMap[id].ticketsRemaining` == 0 && `eventsMap[id].attendees[attendeeId]` == 0 for every `attendeeId` .
2. ***Valid state*** - `defEventCreated` => `eventsMap[id].owner` != 0 & `eventsMap[id].ticketPrice`!= 0 .
4. ***Valid state*** - `defOfferingNotAvailable` => `offerings[id].buyer` == 0  && `offerings[id].price` == 0 && `offerings[id].deadline` == 0 .
5. ***Valid state*** - `defOfferingCreated` => `offerings[id].buyer` != 0  && `offerings[id].price` > 0 && `offerings[id].deadline` > 0 .


6. ***State transitions*** - The only allowed state transitions are : 
    - `defEventNonCreated` to `defEventCreated` only after a call to `createEvent()`.
    - `defOfferingNotAvailable` to `defOfferingAvailable` only after a call to `offerTicket()`.
    - `defOfferingAvailable` to `defOfferingNotAvailable` only after a call to `buyOfferedTicket()`.


7. ***Variable transition*** - `eventsMap[eventId].owner` and `eventsMap[eventId].ticketPrice` and cannot be changed if state is `defEventCreated`.
8. ***Variable transition*** - `eventsMap[eventId].owner` and `eventsMap[eventId].ticketPrice` and can only change if state is `defEventNonCreated` after a call to `createEvent`.
9. ***Variable transition*** - `eventsMap[eventId].ticketsRemaining`  cannot be decreased if state is `defEventCreated`.
10. ***Variable transition*** - `eventsMap[eventId].ticketsRemaining`  can only be decreased if state is `defEventNonCreated` after a call to `createEvent`.


10. ***High-level*** - No way to buy new tickets if `eventsMap[eventId].ticketsRemaining` is 0. 
11. ***High-level*** - No way to offer same tickets multiple times ang be able to sell it after it's sold. 



12. ***Unit tests***  : 
    - `createEvent()` correctly changes state of `eventsMap[eventId]` if state is `defEventNonCreated`.
    - `buyNewTicket(eventId)` correctly changes state of `eventsMap[eventId]` variables if state is `defEventCreated`.
    - `offerTicket(offerId)` correctly changes state of `offerings[offerId]` if state is `defOfferingNotAvailable`.
    
13. ***Unit tests***  : 
- `buyOfferedTicket(offerId)` correctly changes state of `offerings[offerId]` `eventsMap[eventId].attendees[attendeeId]` and if state is `defOfferingAvailable`.
    


</br>

---

## Prioritizing

</br>



### High Priority:

- Property 1 to 11 are high priority because if they fail, the idea of the system fails.
- Property 13 is high priority because it involves testing a function that is supposed to modify both offering and event variables.


### Low Priority:
- Property 12 is low priority because increasing number of participants doesn't affect the system in a very negative way other than accounting for participants number.

- Properties 12 is low priority since:
    1. They check implementation of a specific function (as oppose to multiple functions).
    2. They fairly simple to check by other means, including by manual reviewing of the code.