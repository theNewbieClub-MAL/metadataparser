# SPDX-License-Identifier: MIT

"""Color module for tncpas_metadata."""

import colorsys

from typing import Tuple

class ColorConverter:
    """Converts a hex color value to decimal, rgb, hsv, and hsl values."""
    def __init__(self, hex_value: str):
        """Initialize the ColorConverter class.
        
        :param hex_value: The hex color value to convert.
        :type hex_value: str
        """
        self.hex_value = hex_value

    @property
    def to_dec(self) -> int:
        """Convert the hex color value to decimal."""
        return int(self.hex_value[1:], 16)

    @property
    def to_rgb(self) -> Tuple[int, int, int]:
        """Convert the hex color value to rgb"""
        r = self.to_dec >> 16
        g = (self.to_dec >> 8) & 0xff
        b = self.to_dec & 0xff
        return (r, g, b)

    @property
    def to_hsv(self):
        """Convert the hex color value to hsv"""
        r, g, b = self.to_rgb
        return colorsys.rgb_to_hsv(r, g, b)

    @property
    def to_hsl(self):
        """Convert the hex color value to hsl"""
        r, g, b = self.to_rgb
        return colorsys.rgb_to_hls(r, g, b)

    def __str__(self):
        """Return string representation of ColorConverter class."""
        return self.hex_value

    def __repr__(self):
        """Return string representation of ColorConverter class."""
        return self.hex_value
