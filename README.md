# BITS Cab Share

This is a command line app in python for sharing cabs to Delhi airport and Jaipur at the end of sem. Students add a request and wait in a queue, and when a cab is sent the seniors waiting for that trip get the seats first.

## How to run

You need python 3, nothing else to install (so no requirements.txt)

Open the terminal inside the project folder and run

```
python3 main.py
```

on windows it is `python main.py`

## Menu

1. Add a ride request - it asks name, destination, time slot and year. the student goes into the waiting list, no cab is given yet
2. View waiting students and all cabs - shows who is waiting and all the cabs with seats like 3/4 and if it has left or not
3. Find matches - shows who will get a seat in each open cab if it leaves now. this is only a preview and nothing changes
4. Dispatch a cab - you give destination and time slot, the first open cab for that trip gets filled with the senior most students and leaves
5. Quit

If you type a wrong city or time slot or year like 7 it tells you and asks again, it doesn't crash. small/capital letters don't matter so `delhi` also works.

## Cab file

The cabs are in `data/cabs.json`. I made up the cabs myself. each cab looks like this

```json
{
  "id": "C1",
  "driver": "Aadi",
  "seats": 4,
  "destination": "Delhi",
  "time_slot": "Morning"
}
```

- id - short name of the cab, should be different for every cab
- driver - name of the driver
- seats - 1 to 4
- destination - Delhi or Jaipur
- time_slot - Morning, Afternoon, Evening or Night

The app always goes through the cabs in the same order as this file so the result is same every time. If the file is not there or some cab has wrong values the app tells you and stops.

## Files

- models.py has the RideRequest and Cab classes and the functions that check the input
- dispatcher.py has CabManager which has the queues and does the matching and dispatch
- storage.py loads the cab file
- main.py is the menu

## How seniors first works

There is one priority queue for every destination + time slot, so 8 queues. The queue is for the trip and not for a cab.

I used heapq. heapq is a min heap so it gives the smallest thing first, so I store the year as negative. What I push is

```python
(-year, number, request)
```

5th year becomes -5 which is the smallest so they come out first. number is just a counter (1, 2, 3...) that every request gets when it is added. if two students have the same year then python checks the number and the smaller one (who asked first) comes out first. Also the number is never same for two requests so python never has to compare the request objects, which would give a TypeError.

I didn't use the time for this because 2 requests can come in the same second.

Find matches makes a copy of the queues and pops from the copy, same way as dispatch does. so the preview shows the same students that dispatch will take and the real queues don't change.

## Tricky situations

### 1. Half empty cab

It is allowed. The cab takes whoever is waiting (max its seats) and leaves, so a 4 seater can go with 1 student and it shows 1/4. The empty seats are wasted because nobody can be added after it has left. But a cab can't leave with 0 students, the app just says nobody is waiting.

### 2. No cabs left

The request is still taken and the student goes in the queue. The app tells that there is no open cab for this trip right now. In the waiting list it shows "(no cab for this trip right now)" next to that trip. If you try to dispatch it says no open cab and how many are still waiting. Nobody gets removed from the queue.

### 3. Same year

Same as explained above, the heap has (-year, number, request) so if the year is same the number decides and whoever asked first gets the seat.

### 4. Lots of students

n = students waiting for one trip, N = all students, C = number of cabs

- adding one request is O(log n) because it is one heappush and the item only moves up the heap which has height log n. finding the queue is a dictionary lookup so O(1)
- adding all 1000 is O(N log N), N pushes and each one is O(log N) at most
- sending one cab is O(log n). it pops max 4 students and each pop is O(log n), 4 is a constant
- finding an open cab is O(C) because it loops through the list of cabs till it finds an open one for that trip. cabs are very few so this is fine. it can be made O(1) if we keep a list of open cabs for each trip

## Note

The app does not save anything, when you quit everything is gone and next time it starts again from the cab file.
