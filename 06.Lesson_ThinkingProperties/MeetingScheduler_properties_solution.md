# Properties For MeetingScheduler

First, let us define the states of the Meeting system:

```ruby
- `defUNINITIALIZED` - is defined as `meetings[meetingId].status` is `UNINITIALIZED`.
- `defPENDING`       - is defined as `meetings[meetingId].status` is `PENDING`  .
- `defSTARTED`       - is defined as `meetings[meetingId].status` is `STARTED` .
- `defENDED`         - is defined as `meetings[meetingId].status` is `ENDED`.
- `defCANCELLED`     - is defined as `meetings[meetingId].status` is `CANCELLED` .
```

1. ***Valid state*** - `defUNINITIALIZED` => `getStateById(id)` returns 0 && `getStartTimeById(id)` == `getEndTimeById(id)` == `getNumOfParticipants(id)` == `getOrganizer(id)` == 0 .


2. ***Valid state*** - `defPENDING` => `getStateById(id)` returns 1 && `getStartTimeById(id)` > `getEndTimeById(id)` > 0 &&`getNumOfParticipants(id)` == 0 && `getOrganizer(id)` != 0 .
3. ***Valid state*** - `defSTARTED` => `getStateById(id)` returns 2 && `getStartTimeById(id)` > `getEndTimeById(id)` > 0 &&`getOrganizer(id)` != 0 .
4. ***Valid state*** - `defENDED` => `getStateById(id)` returns 3 && `getStartTimeById(id)` > `getEndTimeById(id)` > 0  && `getOrganizer(id)` != 0 .
5. ***Valid state*** - `defCANCELLED` => `getStateById(id)` returns 4 && `getStartTimeById(id)` > `getEndTimeById(id)` > 0 &&`getNumOfParticipants(id)` == 0 && `getOrganizer(id)` != 0.


6. ***State transitions*** - The only allowed state transitions are : 
    - `defUNINITIALIZED` to `defPENDING` only after a call to `scheduledMeeting()`.
    - `defPENDING` to `defSTARTED` only after a call to `startMeeting()`.
    - `defPENDING` to `defCANCELLED` only after a call to `cancelMeeting()`.
    - `defSTARTED` to `defENDED` only after a call to `endMeeting()`.

7. ***Variable transition*** - `meetings[meetingId].startTime` and `meetings[meetingId].endTime` and `meetings[meetingId].numOfParticipants` cannot be decreased.

8. ***Variable transition*** - `meetings[meetingId].startTime` and `meetings[meetingId].endTime` can only increase after a call to `scheduledMeeting()`.

9. ***Variable transition*** - `meetings[meetingId].numOfParticipants` can only increase after a call to `joinMeeting()`.



10. ***High-level*** - No way to create a meeting if `meetings[meetingId].startTime` < now or `meetings[meetingId].startTime` > `meetings[meetingId].endTime` or  state is not `defUNINITIALIZED`. 
11. ***High-level*** - No way to start a meeting if `meetings[meetingId].startTime` > now or state is not `defPENDING`. 
12. ***High-level*** - No way to end a meeting if `meetings[meetingId].endTime` < now or or state is not `defSTARTED`. 
13. ***High-level*** - No way to cancel a meeting if state is not `defPENDING` or `msg'sender` is not the owner. 
14. ***High-level*** - No way to join a meeting if state is not `defSTARTED`. 




15. ***Unit tests*** - transitions : 
    - `scheduledMeeting(meetingId)` correctly changes state of `meetings[meetingId]` if state is `defUNINITIALIZED`.
    - `startMeeting(meetingId)` correctly changes state of `meetings[meetingId]` if state is `defPENDING`.
    - `endMeeting(meetingId)` correctly changes state of `meetings[meetingId]` if state is `defSTARTED`.
    - `cancelMeeting(meetingId)` correctly changes state of `meetings[meetingId]` if state is `defPENDING`.
    

16. ***Unit tests*** - joinMeeting() correctly increases `meetings[meetingId].numOfParticipants` if state is `defSTARTED`.

</br>

---

## Prioritizing

</br>



### High Priority:

- Property 1 to 8 & 10 to 13 are high priority because if they fail, the idea of the system fails.


### Low Priority:
- Property 9 is low priority because increasing number of participants doesn't affect the system in a very negative way other than accounting for participants number.

- Properties 15 & 16 are low priority since:
    1. They check implementation of a specific function (as oppose to multiple functions).
    2. They fairly simple to check by other means, including by manual reviewing of the code.