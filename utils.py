import re

def validate_part_id(part_id):
    """Uses Regex to ensure Part ID follows engineering standards"""
    pattern = r"^[A-Z]{4}-\d{4}$"
    if re.match(pattern, part_id):
        return True
    return False