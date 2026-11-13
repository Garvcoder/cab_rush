import json
from models import Cab, check_destination, check_time_slot, check_number


def load_cabs(filename):
    try:
        f = open(filename)
        data = json.load(f)
        f.close()
    except FileNotFoundError:
        print("cant find the cab file", filename)
        return None
    except json.JSONDecodeError:
        print("something is wrong with the json in", filename)
        return None

    cabs = []
    ids = []
    try:
        for c in data:
            cab_id = str(c["id"])
            seats = check_number(c["seats"], 1, 4)
            dest = check_destination(c["destination"])
            slot = check_time_slot(c["time_slot"])
            if seats == None or dest == None or slot == None:
                print("cab", cab_id, "in the file has wrong seats or destination or time slot")
                return None
            if cab_id in ids:
                print("cab id", cab_id, "is written twice in the file")
                return None
            ids.append(cab_id)
            cabs.append(Cab(cab_id, str(c["driver"]), seats, dest, slot))
    except (KeyError, TypeError):
        print("one of the cabs in the file is missing something (id, driver, seats, destination, time_slot)")
        return None
    return cabs
