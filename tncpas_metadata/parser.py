# SPDX-License-Identifier: MIT

"""TNCPAS-0001 Compliance Metadata Parser Module"""

import re
from typing import Any, Dict, List, Optional

from .color import ColorConverter
from .definition import definitions, EditionMetadata, StaffEntry
from .errors import NoMetadataBlockFoundError, ItemExceedsGlobalLimitError


class MetadataParser:
    """Class to parse TNCPAS-0001 Compliance metadata to preferred format"""

    def __init__(
        self,
        string: str,
        custom_definition: Optional[Dict[str, Dict[str, Any]]] = None
    ):
        """
        Parse metadata from a string.

        :param string: The string to parse metadata from.
        :type string: str
        :param custom_definition: Custom definition to use for parsing metadata.
        :type custom_definition: Optional[Dict[str, Dict[str, Any]]]
        """
        self.string = string
        self.definition = definitions
        self.custom_definition = custom_definition
        if custom_definition is not None:
            self.definition.update(self.custom_definition)  # type: ignore

    def _parse_value(self, key: str, value: str) -> Any:
        """
        Parse a value from a key.

        :param key: The key to parse value from.
        :type key: str
        :param value: The value to parse.
        :type value: str
        :return: The parsed value.
        :rtype: Any
        """
        if ';' in value:
            values = [self._parse_single_value(
                key, v) for v in value.split(';')]
            # convert 0 to None
            values = [None if v == 0 else v for v in values]
            if len(values) == 1:
                return values[0]
            return values
        else:
            return self._parse_single_value(key, value)

    def _parse_single_value(self, key: str, value: str) -> Any:
        """
        Parse a single value from a key.

        :param key: The key to parse value from.
        :type key: str
        :param value: The value to parse.
        :type value: str
        :return: The parsed value.
        :rtype: Any
        """
        keydef = self.definition.get(key, {})
        keyname = keydef.get('key_name', key)
        if '|' in value:
            if key == "LIM":
                return [int(v) if v.isdigit() else None for v in value.split('|')][:2]
            else:
                raise ValueError(
                    f"Invalid value {value} found in metadata on key \"{keyname}\".")
        elif value.isdigit():
            return int(value)
        elif value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        elif key == 'THM' and value:
            return value.strip()
        else:
            return value

    @property
    def raw_metadata(self) -> List[str]:
        """
        Return raw metadata from string.

        :return: The raw metadata.
        :rtype: List[str]
        """
        check = re.search(r'###(METADATA|SCRAPEDATA)', self.string)
        if check is None:
            raise NoMetadataBlockFoundError(
                "No metadata block found in string.")

        block = self.string[check.start():]
        block = block.split('###')[1]
        block = re.sub(r'\s?{-(.*?)-}\s?', '', block)  # Remove comments
        block = block.strip()
        block = re.sub(r'>>>', '\n>>>', block)
        block = block.splitlines()
        block = [line for line in block if line != '']
        block = [line.strip() for line in block]
        block.pop(0)
        return block

    @property
    def return_metadata(self) -> Dict[str, Any]:
        metadata: Dict[str, Any] = {}
        metadata['custom'] = {}
        global_total_items = 0

        for item in self.raw_metadata:
            key, value = item.strip().replace('>>>', '').split('>>')
            key = key.upper()
            value = self._parse_value(key, value)

            keydef = self.definition.get(key, {})
            keyname = keydef.get('key_name', key)
            is_global_item = keydef.get('follow_global_items', False)

            if self.custom_definition is not None and key in self.custom_definition:
                metadata['custom'][keyname] = value
            else:
                metadata[keyname] = value  # type: ignore

            if is_global_item and isinstance(value, list):
                if global_total_items == 0:
                    global_total_items = len(value)  # type: ignore
                elif global_total_items != len(value):  # type: ignore
                    raise ItemExceedsGlobalLimitError(
                        f"Invalid number of items found in metadata on key \"{keyname}\". Expected {global_total_items}, got {len(value)}."  # type: ignore
                    )
        # if required items are missing, raise an error
        for key, value in self.definition.items():
            keyname = value.get('key_name', key)
            hint = f'"{key}"'
            if keyname != key:
                hint = f'"{keyname}" ({key})'
            if value.get('required', False) and keyname not in metadata:
                raise ValueError(
                    f"Required key {hint} can not be found in metadata.")

        if not metadata['custom']:
            metadata.pop('custom')

        return metadata

    def return_formatted(self, custom_metadata: Optional[Dict[str, Any]] = None) -> EditionMetadata:
        """
        Return a metadata that human-readable

        :param custom_metadata: Custom metadata to be formatted
        :type custom_metadata: Optional[Dict[str, Any]]
        :return: A dataclass of Metadata
        """
        if custom_metadata:
            metadata = custom_metadata
        else:
            metadata = self.return_metadata

        # get staff length, drop None values
        staff_length = len([v for v in metadata['staff'] if v is not None])
        staffs: List[StaffEntry] = []
        
        for index in range(staff_length):
            staffs.append(StaffEntry(
                nickname=metadata['staff'][index],
                available=metadata['available'][index],
                limit=metadata['limit'][index],
                identifier=metadata.get('identifier', [None])[index],
                is_allow_slip=metadata.get('is_allow_slip', [True])[index]
            ))

        colors = metadata.get('color', [])
        if len(colors) == 0:
            colors = None
        elif isinstance(colors, ColorConverter):
            colors = [colors]
        elif isinstance(colors, str):
            colors = [ColorConverter(colors)]
        elif isinstance(colors, list):
            colors = [ColorConverter(c) if isinstance(c, str) else c for c in colors]  # type: ignore

        return EditionMetadata(
            theme=metadata['theme'],
            maximum=metadata['maximum'],
            staffs=staffs,
            theme_id=metadata.get('theme_id', None),
            theme_emoji=metadata.get('theme_emoji', None),
            colors=colors or None,  # type: ignore
            custom=metadata.get('custom', None)
        )
