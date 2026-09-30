def convert_time_to_minutes(scan_time):
    """Convert a validated HH:MM time to minutes after midnight."""
    hour, minute = map(int, scan_time.split(":"))
    return hour * 60 + minute


def determine_attendance_status(scan_time):
    """Classify a scan as EARLY, ON TIME, or LATE."""
    total = convert_time_to_minutes(scan_time)
    early_limit = 7 * 60 + 30
    on_time_limit = 8 * 60

    if total < early_limit:
        return "EARLY"
    if total <= on_time_limit:
        return "ON TIME"
    return "LATE"


def validate_time(scan_time):
    """Return True only for a 24-hour HH:MM time with valid ranges."""
    if not isinstance(scan_time, str):
        return False

    parts = scan_time.split(":")
    if (
        len(parts) != 2
        or any(len(part) != 2 or not part.isdigit() for part in parts)
    ):
        return False

    hour, minute = map(int, parts)
    return 0 <= hour <= 23 and 0 <= minute <= 59
