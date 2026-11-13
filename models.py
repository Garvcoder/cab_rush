from datetime import datetime

DESTINATIONS = ["Delhi", "Jaipur"]
TIME_SLOTS = ["Morning", "Afternoon", "Evening", "Night"]


def check_destination(text):
    text = str(text).strip().lower()
    if text == "delhi":
        return "Delhi"
    elif text == "jaipur":
        return "Jaipur"
    else:
        return None


def check_time_slot(text):
    text = str(text).strip().lower()
    for slot in TIME_SLOTS:
        if slot.lower() == text:
            return slot
    return None


def check_number(text, smallest, biggest):
    try:
        n = int(str(text).strip())
    except ValueError:
        return None
    if n >= smallest and n <= biggest:
        return n
    return None


class RideRequest:
    def __init__(self, name, destination, time_slot, year, number, submitted_at=None):
        self.name = name
        self.destination = destination
        self.time_slot = time_slot
        self.year = year
        self.number = number
        if submitted_at == None:
            submitted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.submitted_at = submitted_at

    def __str__(self):
        return f"{self.name} (Year {self.year}, request #{self.number}, asked at {self.submitted_at})"


class Cab:
    def __init__(self, cab_id, driver, seats, destination, time_slot):
        self.cab_id = cab_id
        self.driver = driver
        self.seats = seats
        self.destination = destination
        self.time_slot = time_slot
        self.has_left = False
        self.passengers = []

    def free_seats(self):
        return self.seats - len(self.passengers)

    def add_passenger(self, request):
        if self.has_left == True:
            return False
        if self.free_seats() == 0:
            return False
        self.passengers.append(request)
        return True

    def __str__(self):
        status = "open"
        if self.has_left == True:
            status = "LEFT"
        taken = len(self.passengers)
        return f"[{self.cab_id}] {self.driver} | {self.destination}, {self.time_slot} | {taken}/{self.seats} seats | {status}"
