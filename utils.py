import re

def is_valid_part_id(uid):
    """
    Checks if the ID is 4 uppercase letters, a hyphen, and 4 digits.
    Example: MECH-1234
    """
    pattern = r"^[A-Z]{4}-\d{4}$"
    return bool(re.match(pattern, uid))