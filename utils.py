import re

def is_valid_part_id(uid):

    pattern = r"^[A-Z]{4}-\d{4}$"
    return bool(re.match(pattern, uid))