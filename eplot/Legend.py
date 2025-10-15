from typing import Union
from enum import Enum, IntEnum
import matplotlib.pyplot as plt


class Position(IntEnum):
    Best = 0
    UpperLeft = 2
    UpperCenter = 9
    UpperRight = 1
    CenterLeft = 6
    CenterCenter = 10
    CenterRight = 7
    LowerLeft = 3
    LowerCenter = 8
    LowerRight = 4
    OutsideUpper = 11
    OutsideCenter = 12
    OutsideLower = 13


class LegFontSize(Enum):
    XXS = "xx-small"
    XS = "x-small"
    S = "small"
    M = "medium"
    L = "large"
    XL = "x-large"
    XXL = "xx-large"


class Legend:
    _le_pos = None
    _bbox_anchor = None
    y2mode = False

    @property
    def LegendPos(self):
        return self._le_pos

    @LegendPos.setter
    def LegendPos(self, value: Union[int, Position]):
        if value == Position.OutsideUpper:
            self._le_pos = Position.UpperLeft
            self._bbox_anchor = (1.2, 1.0) if self.y2mode else (1.02, 1.0)
        elif value == Position.OutsideCenter:
            self._le_pos = Position.CenterLeft
            self._bbox_anchor = (1.2, 0.5) if self.y2mode else (1.02, 0.5)
        elif value == Position.OutsideLower:
            self._le_pos = Position.LowerLeft
            self._bbox_anchor = (1.2, 0.0) if self.y2mode else (1.02, 0.0)
        else:
            self._le_pos = value

    def set_legend(self, axes: plt.Axes, handle: list, label: list, loc: Union[int, Position], fsize: LegFontSize = LegFontSize.M, y2mode: bool = False):
        self.y2mode = y2mode
        self.LegendPos = loc
        if int(loc) <= 10:
            axes.legend(handle, label, fontsize=fsize.value, loc=self.LegendPos)
        else:
            axes.legend(handle, label, fontsize=fsize.value, loc=self.LegendPos, bbox_to_anchor=self._bbox_anchor, borderaxespad=0)
