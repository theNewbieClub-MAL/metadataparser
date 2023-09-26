# SPDX-License-Identifier: MIT

"""TNCPAS-0001 Compliance Metadata Parser Module"""

from .definition import EditionMetadata, StaffEntry
from .errors import (ForbiddenListInListError, ItemExceedsGlobalLimitError,
                     MissingRequiredKey, MissingRequiredKeyError,
                     NoMetadataBlockFoundError)
from .identifier import EditionIdentifier, StaffIdentifier
from .parser import MetadataParser

__version__ = '0.2.0'

__all__ = [
    "EditionIdentifier",
    "EditionMetadata",
    "ForbiddenListInListError",
    "ItemExceedsGlobalLimitError",
    "MetadataParser",
    "MissingRequiredKey",  # Alias for backwards compatibility
    "MissingRequiredKeyError",
    "NoMetadataBlockFoundError",
    "StaffEntry",
    "StaffIdentifier",
]
