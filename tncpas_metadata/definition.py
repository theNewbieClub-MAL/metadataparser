# SPDX-License-Identifier: MIT

"""Definition of TNCPAS-0001 Compliance Metadata"""

from typing import List, Union, Optional
from dataclasses import dataclass

from .color import ColorConverter as Color

definitions = {
    "AVA": {
        "key_name": "available",
        "key_type": List[Union[int, None]],
        "required": True,
        "follow_global_items": True,
        "description": "Total number of cards designer by the contributors/staff in a release",
    },
    "CLR": {
        "key_name": "color",
        "key_type": Optional[List[Union[str, None]]],
        "required": False,
        "follow_global_items": False,
        "description": "Font colors used on a thread in Hex format",
    },
    "LIM": {
        "key_name": "limit",
        "key_type": List[Union[int, List[int]]],
        "required": True,
        "follow_global_items": True,
        "description": "Maximum number of cards an user can have in a release per contributor/staff",
    },
    "MAX": {
        "key_name": "maximum",
        "key_type": int,
        "required": False,
        "description": "Maximum requests to accept in a release",
    },
    "SID": {
        "key_name": "staff_id",
        "key_type": List[Union[int, str]],
        "required": False,
        "follow_global_items": True,
        "description": "Staff/Contributor ID",
    },
    "SLP": {
        "key_name": "is_allow_slip",
        "key_type": List[bool],
        "required": False,
        "follow_global_items": True,
        "description": "Whether or not the staff/contributor allows slip",
    },
    "STF": {
        "key_name": "staff",
        "key_type": List[str],
        "required": True,
        "follow_global_items": True,
        "description": "Staff/Contributor name",
    },
    "TEM": {
        "key_name": "theme_emoji",
        "key_type": str,
        "required": False,
        "description": "Edition title/theme emoji",
    },
    "THM": {
        "key_name": "theme",
        "key_type": str,
        "required": True,
        "description": "Edition title/theme",
    },
    "TID": {
        "key_name": "theme_id",
        "key_type": Union[int, str],
        "required": False,
        "description": "Edition ID",
    },
}

@dataclass
class StaffEntry:
    """Information about staff"""
    nickname: str
    """Nickname of the staff/contributor"""
    available: int
    """Total card available to choose"""
    limit: Union[int, List[int]]
    """Limit of card for each user"""
    identifier: Optional[List[Union[str, int]]] = None
    """Staff/contributor identifier"""
    is_allow_slip: Optional[bool] = True
    """Is staff/contributor allows slip use"""

@dataclass
class EditionMetadata:
    """Metadata of the edition"""
    theme: str
    """Edition title/theme"""
    maximum: int
    """Maximum requests per edition"""
    staffs: List[StaffEntry]
    """List of participated staff/contributors"""
    theme_id: Union[int, str, None] = None
    """Edition ID"""
    theme_emoji: Optional[str] = None
    """Edition title/theme emoji"""
    colors: Union[List[Color], Color, None] = None
    """Font colors used on a thread in Hex format"""
    custom: Any = None
    """Custom data"""
