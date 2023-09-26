# SPDX-License-Identifier: MIT

"""Error classes for tncpas_metadata."""

class NoMetadataBlockFoundError(Exception):
    """Raised when no metadata block is found in the string."""

class ItemExceedsGlobalLimitError(Exception):
    """Raised when an item exceeds the global limit."""

class ForbiddenListInListError(Exception):
    """Raised when a list is found in a list other than the LIM key."""

class MissingRequiredKeyError(Exception):
    """Raised when key required by parser is missing"""

MissingRequiredKey = MissingRequiredKeyError
