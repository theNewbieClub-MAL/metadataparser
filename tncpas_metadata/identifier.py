# SPDX-License-Identifier: MIT

"""Identifier module for tncpas_metadata."""

from datetime import datetime


class StaffIdentifier:
    """Class for creating staff identifiers."""

    def __init__(self, staff_id: str):
        """Initialize StaffIdentifier class."""
        self.staff_id = staff_id

    @property
    def year(self) -> int:
        """Get the year from the staff ID."""
        return datetime.strptime(self.staff_id[:2], "%y").year

    @property
    def month(self) -> int:
        """Get the month from the staff ID."""
        return datetime.strptime(self.staff_id[2:5], "%b").month

    @property
    def sequence(self) -> int:
        """Get the sequence from the staff ID."""
        # convert A-Z to 1-26
        return (ord(self.staff_id[5]) - 64)

    @property
    def edition_id(self) -> str:
        """Get the edition ID from the staff ID."""
        return self.staff_id[6:9]

    @property
    def user_id(self) -> str:
        """Get the user ID from the staff ID."""
        return self.staff_id[9:]

    def __str__(self):
        """Return string representation of StaffIdentifier class."""
        return self.staff_id

    def __repr__(self):
        """Return string representation of StaffIdentifier class."""
        return self.staff_id


class EditionIdentifier:
    """Class for creating edition identifiers."""

    def __init__(self, edition_id: str):
        """Initialize EditionIdentifier class."""
        self.edition_id = edition_id

    @property
    def year(self) -> int:
        """Get the year from the edition ID."""
        return datetime.strptime(self.edition_id[:2], "%y").year

    @property
    def month(self) -> int:
        """Get the month from the edition ID."""
        return datetime.strptime(self.edition_id[2:4], "%m").month

    @property
    def sequence(self) -> int:
        """Get the sequence from the edition ID."""
        # convert A-Z to 1-26
        return (ord(self.edition_id[4]) - 64)

    def __str__(self):
        """Return string representation of EditionIdentifier class."""
        return self.edition_id

    def __repr__(self):
        """Return string representation of EditionIdentifier class."""
        return self.edition_id
