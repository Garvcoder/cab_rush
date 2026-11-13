from dispatcher import CabManager
from models import DESTINATIONS, TIME_SLOTS, check_destination, check_time_slot, check_number
from storage import load_cabs

CAB_FILE = "data/cabs.json"


def ask_destination():
    while True:
        dest = check_destination(input("Destination (Delhi / Jaipur): "))
        if dest != None:
            return dest
        print("we only go to delhi or jaipur, type one of those")


def ask_time_slot():
    while True:
        slot = check_time_slot(input("Time slot (Morning / Afternoon / Evening / Night): "))
        if slot != None:
            return slot
        print("no such time slot, pick from the 4 above")


def add_request(manager):
    name = input("Student name: ").strip()
    while name == "":
        print("you forgot the name")
        name = input("Student name: ").strip()

    dest = ask_destination()
    slot = ask_time_slot()

    year = check_number(input("Year (1 to 5): "), 1, 5)
    while year == None:
        print("year should be between 1 and 5")
        year = check_number(input("Year (1 to 5): "), 1, 5)

    manager.add_request(name, dest, slot, year)
    n = len(manager.get_waiting(dest, slot))
    print(f"ok {name} is on the waiting list for {dest} {slot}, total {n} waiting for this trip")
    if manager.find_open_cab(dest, slot) == None:
        print("btw there is no cab for this trip right now so", name, "has to wait")


def show_waiting(manager):
    print()
    print("--- Waiting students (" + str(manager.count_waiting()) + ") ---")
    if manager.count_waiting() == 0:
        print("no one is waiting")
    for dest in DESTINATIONS:
        for slot in TIME_SLOTS:
            waiting = manager.get_waiting(dest, slot)
            if len(waiting) > 0:
                if manager.find_open_cab(dest, slot) == None:
                    print(dest + ", " + slot + ":  (no cab for this trip right now)")
                else:
                    print(dest + ", " + slot + ":")
                i = 1
                for request in waiting:
                    print("  " + str(i) + ". " + str(request))
                    i = i + 1


def show_cabs(manager):
    print()
    print("--- Cabs ---")
    for cab in manager.cabs:
        print(cab)
        for p in cab.passengers:
            print(f"      - {p.name} (Year {p.year})")


def show_matches(manager):
    print()
    print("--- who gets a seat if the cabs leave now (just a preview) ---")
    matches = manager.find_matches()
    if len(matches) == 0:
        print("all the cabs have left")
    for m in matches:
        cab = m[0]
        students = m[1]
        print(cab)
        if len(students) == 0:
            print("      (no one waiting for this cab)")
        for s in students:
            print("      - " + str(s))


def dispatch_cab(manager):
    dest = ask_destination()
    slot = ask_time_slot()
    waiting = manager.get_waiting(dest, slot)

    if manager.find_open_cab(dest, slot) == None:
        print(f"there is no cab left for {dest} {slot}, so nothing happened")
        print("still waiting for this trip:", len(waiting))
        return
    if len(waiting) == 0:
        print(f"no one is waiting for {dest} {slot}, cab is not going empty")
        return

    cab = manager.dispatch(dest, slot)

    print(f"cab {cab.cab_id} ({cab.driver}) has left for {dest} {slot} with {len(cab.passengers)}/{cab.seats} seats full, people in it:")
    for p in cab.passengers:
        print(f"  - {p.name} (Year {p.year})")
    left = len(manager.get_waiting(dest, slot))
    if left > 0:
        print("still waiting for this trip:", left)


def main():
    cabs = load_cabs(CAB_FILE)
    if cabs == None:
        print("fix the cab file and then run it again")
        return
    print("got", len(cabs), "cabs from the file")

    manager = CabManager(cabs)

    try:
        while True:
            print()
            print("===== BITS Cab Share =====")
            print("1. Add a ride request")
            print("2. View waiting students and all cabs")
            print("3. Find matches (preview)")
            print("4. Dispatch a cab")
            print("5. Quit")
            choice = input("what do you want to do? (1-5): ").strip()

            if choice == "1":
                add_request(manager)
            elif choice == "2":
                show_waiting(manager)
                show_cabs(manager)
            elif choice == "3":
                show_matches(manager)
            elif choice == "4":
                dispatch_cab(manager)
            elif choice == "5":
                break
            else:
                print("thats not an option, type 1 to 5")
    except (KeyboardInterrupt, EOFError):
        print()

    print("ok bye!")


if __name__ == "__main__":
    main()
