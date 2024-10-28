from typing import Union
from enum import IntEnum
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


class Legend:
    @property
    def LegendPos(self):
        return self._le_pos

    @LegendPos.setter
    def LegendPos(self, value: Union[int, Position]):
        if value == Position.OutsideUpper:
            self._le_pos = Position.UpperLeft
            self._bbox_anchor = (1.02, 1.0,)
        elif value == Position.OutsideCenter:
            self._le_pos = Position.CenterLeft
            self._bbox_anchor = (1.02, 0.5,)
        elif value == Position.OutsideLower:
            self._le_pos = Position.LowerLeft
            self._bbox_anchor = (1.02, 0.0,)
        else:
            self._le_pos = value

    def set_legend(self, axes: plt.Axes, handle, label, loc: Union[int, Position]):
        LegendPos = loc
        if int(loc) <= 10:
            axes.legend(handle, label, loc=self.LegendPos)
        else:
            axes.legend(loc=self.LegendPos, bbox_to_anchor=self._bbox_anchor, borderaxespad=0)
