def parse_ride_duration(text):
    """
    Converts a ride duration written as HH:MM into minutes.
    Returns an int, or None if the input is not a valid HH:MM string.
    """
    if not isinstance(text, str):
        return None
    parts = text.strip().split(':')
    if len(parts) != 2:
        return None
    hours, minutes = parts[0].strip(), parts[1].strip()
    # isdecimal() accepts only characters int() can convert (no '-', '_', '²' etc.)
    if not (hours.isdecimal() and minutes.isdecimal()):
        return None
    try:
        hours, minutes = int(hours), int(minutes)
    except ValueError:  # e.g. absurdly long digit strings hitting Python's int limit
        return None
    if minutes >= 60:
        return None
    return hours * 60 + minutes


def format_station_code(code):
    """
    Formats a station code as ZONE-NUMBER, e.g. 'a12' -> 'A-12'.
    Returns a string, or None if the input is not a usable station code.
    """
    if not isinstance(code, str):
        return None
    code = code.strip().upper()
    if len(code) < 2:  # need at least a zone letter and a number
        return None
    return code[0] + '-' + code[1:]


def parse_ride_log(line):
    """
    Parses 'bike_type,minutes,subscriber' into a tuple.
    Returns (bike_type, minutes, is_subscriber), or None if the line is malformed.
    """
    if not isinstance(line, str):
        return None
    parts = line.split(',')
    if len(parts) != 3:
        return None
    bike_type, minutes, subscriber = (p.strip() for p in parts)
    if not bike_type or not minutes.isdecimal():
        return None
    try:
        minutes = int(minutes)
    except ValueError:
        return None
    return bike_type, minutes, subscriber.lower() == 'yes'


def _show(label, result):
    if result is None:
        print(f"{label} Invalid input")
    else:
        print(label, result)


def main():
    print("==== Running parse_ride_duration ====")
    value = input("Enter a ride duration as HH:MM (e.g. 01:15): ")
    _show("Duration in minutes:", parse_ride_duration(value))

    print("\n==== Running format_station_code ====")
    value = input("Enter a station code (e.g. a12): ")
    _show("Formatted station code:", format_station_code(value))

    print("\n==== Running parse_ride_log ====")
    value = input("Enter a ride log line as type,minutes,subscriber (e.g. electric,45,yes): ")
    _show("Parsed ride log:", parse_ride_log(value))


if __name__ == "__main__":
    main()
