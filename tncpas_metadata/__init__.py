# SPDX-License-Identifier: MIT

"""TNCPAS-0001 Compliance Metadata Parser Module"""

from .definition import EditionMetadata, StaffEntry
from .errors import (ItemExceedsGlobalLimitError, MissingRequiredKey,
                     NoMetadataBlockFoundError)
from .identifier import EditionIdentifier, StaffIdentifier
from .parser import MetadataParser

__version__ = '0.1.0'

__all__ = [
    EditionIdentifier,
    EditionMetadata,
    ItemExceedsGlobalLimitError,
    MetadataParser,
    MissingRequiredKey,
    NoMetadataBlockFoundError,
    StaffEntry,
    StaffIdentifier,
]
