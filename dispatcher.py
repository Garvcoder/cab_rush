import heapq
from models import DESTINATIONS, TIME_SLOTS, RideRequest


class CabManager:
    def __init__(self, cabs):
        self.cabs = cabs
        self.next_number = 1

        # one queue for each trip
        self.queues = {}
        for d in DESTINATIONS:
            for t in TIME_SLOTS:
                self.queues[(d, t)] = []

    def put_in_queue(self, request):
        # min heap so year is negative, if year is same the smaller number (asked first) wins
        q = self.queues[(request.destination, request.time_slot)]
        heapq.heappush(q, (-request.year, request.number, request))

    def add_request(self, name, destination, time_slot, year):
        request = RideRequest(name, destination, time_slot, year, self.next_number)
        self.next_number += 1
        self.put_in_queue(request)
        return request

    def get_waiting(self, destination, time_slot):
        q = self.queues[(destination, time_slot)]
        result = []
        for item in sorted(q):
            result.append(item[2])
        return result

    def count_waiting(self):
        count = 0
        for key in self.queues:
            count = count + len(self.queues[key])
        return count

    def find_open_cab(self, destination, time_slot):
        for cab in self.cabs:
            if cab.destination == destination and cab.time_slot == time_slot:
                if cab.has_left == False:
                    return cab
        return None

    def find_matches(self):
        # preview only so use a copy
        copies = {}
        for key in self.queues:
            copies[key] = self.queues[key].copy()

        matches = []
        for cab in self.cabs:
            if cab.has_left == False:
                q = copies[(cab.destination, cab.time_slot)]
                students = []
                seats = cab.free_seats()
                while seats > 0 and len(q) > 0:
                    item = heapq.heappop(q)
                    students.append(item[2])
                    seats = seats - 1
                matches.append((cab, students))
        return matches

    def dispatch(self, destination, time_slot):
        cab = self.find_open_cab(destination, time_slot)
        q = self.queues[(destination, time_slot)]
        if cab == None:
            return None
        if len(q) == 0:
            return None

        while cab.free_seats() > 0 and len(q) > 0:
            item = heapq.heappop(q)
            cab.add_passenger(item[2])
        cab.has_left = True
        return cab
