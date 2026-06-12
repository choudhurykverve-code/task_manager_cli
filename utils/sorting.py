PRIORITY_ORDER = {
    "HIGH": 1,
    "MEDIUM": 2,
    "LOW": 3,
}


def sort_by_priority(tasks):
    """Sort tasks by priority (HIGH first)."""
    return sorted(tasks, key=lambda t: PRIORITY_ORDER[t.priority.value])


def sort_by_created_at(tasks):
    """Sort tasks by creation date."""
    return sorted(tasks, key=lambda t: t.created_at)
