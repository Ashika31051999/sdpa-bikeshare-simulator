import json
import math

def parse_int(text, minimum=None, maximum=None):
    if not isinstance(text, str):
        raise TypeError("Input text must be a string.")
    clean_text = text.strip()
    if not clean_text:
        raise ValueError("Input cannot be empty.")
    try:
        val = int(clean_text)
    except ValueError:
        raise ValueError("Not a valid whole number.")
    if (minimum is not None and val < minimum) or (maximum is not None and val > maximum):
        raise ValueError("Value out of permitted range.")
    return val

def pence_to_pounds(pence):
    if not isinstance(pence, int):
        raise TypeError("Pence must be an integer.")
    sign = "-" if pence < 0 else ""
    abs_pence = abs(pence)
    return f"{sign}£{abs_pence // 100}.{abs_pence % 100:02d}"

def load_days(path):
    with open(path, 'r') as f:
        data = json.load(f)
    if not isinstance(data, list) or len(data) == 0:
        raise ValueError("Invalid days layout list structure.")
    
    result = []
    for day in data:
        if not isinstance(day, list):
            raise ValueError("Day must be a list.")
        day_trips = []
        for trip in day:
            if not isinstance(trip, list) or len(trip) != 3:
                raise ValueError("Trip must have 3 items.")
            o, d, c = trip
            if not isinstance(o, str) or not isinstance(d, str) or not isinstance(c, int) or c < 0:
                raise ValueError("Invalid trip types or values.")
            if o == d:
                raise ValueError("Origin cannot equal destination.")
            day_trips.append((o, d, c))
        result.append(day_trips)
    return result

def completed_trips(requested, bikes, free_docks):
    for val in (requested, bikes, free_docks):
        if not isinstance(val, int):
            raise TypeError("Arguments must be integers.")
        if val < 0:
            raise ValueError("Arguments cannot be negative.")
    return min(requested, bikes, free_docks)

def breakages(completed, rate_percent):
    for val in (completed, rate_percent):
        if not isinstance(val, int):
            raise TypeError("Arguments must be integers.")
        if val < 0:
            raise ValueError("Arguments cannot be negative.")
    if rate_percent > 100:
        raise ValueError("Rate cannot exceed 100.")
    return math.ceil(completed * rate_percent / 100)
