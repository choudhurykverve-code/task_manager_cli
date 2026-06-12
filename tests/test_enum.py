from models.enum import Priority, Status


class TestStatus:

    def test_values(self):
        assert Status.PENDING.value == "PENDING"
        assert Status.COMPLETED.value == "COMPLETED"

    def test_member_count(self):
        assert len(Status) == 2

    def test_lookup_by_name(self):
        assert Status["PENDING"] is Status.PENDING
        assert Status["COMPLETED"] is Status.COMPLETED


class TestPriority:

    def test_values(self):
        assert Priority.LOW.value == "LOW"
        assert Priority.MEDIUM.value == "MEDIUM"
        assert Priority.HIGH.value == "HIGH"

    def test_member_count(self):
        assert len(Priority) == 3

    def test_lookup_by_name(self):
        assert Priority["LOW"] is Priority.LOW
        assert Priority["MEDIUM"] is Priority.MEDIUM
        assert Priority["HIGH"] is Priority.HIGH
