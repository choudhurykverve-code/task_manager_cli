from models.enum import Priority


def parse_priority(value, default=Priority.MEDIUM):
    """Parse a priority string into a Priority enum, with a default fallback."""
    if value:
        return Priority[value.upper()]
    return default
