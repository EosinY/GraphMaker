import matplotlib.pyplot as plt
from typing import Final, Union, Dict, List, Tuple
from enum import Enum, unique


@unique
class PointType(Enum):
    Dot = "."
    Circle = "o"
    UpTriangle = "^"
    DownTriangle = "v"
    Square = "s"
    Cross = "x"
    Plus = "+"

    def Value(e):
        return e.value


@unique
class LineType(Enum):
    Solid = "-"
    Dash = "--"
    DashDot = "-."
    Dot = ":"

    def Value(e):
        return e.value


@unique
class AxisType(Enum):
    Linear = "0"
    Log = "1"

    def Value(e):
        return e.value


class XY_PlotEntry:
    def __init__(
            self,
            x_data: list, y_data: list, name: str, *,
            groupid: str = None,
            color: str = None,
            point: Union[PointType, tuple[PointType, float]] = (PointType.Circle, 1),
            line: Union[LineType, tuple[LineType, float]] = (LineType.Solid, 1.5)):

        self.x_data = x_data
        self.y_data = y_data
        self.name = name

        self.groupid = groupid

        self.color = color
        if point is PointType:
            self.pointtype = point
        else:
            self.pointtype = point[0]
            self.pointsize = point[1]

        if line is LineType:
            self.linetype = line
        else:
            self.linetype = line[0]
            self.linetype = line[1]


class XY2_PlotEntry(XY_PlotEntry):
    def __init__(self, x_data, y_data, y2_data, name, *, groupid=None, color=None, point=(PointType.Circle, 1), line=(LineType.Solid, 1.5)):
        super().__init__(x_data, y_data, name, groupid=groupid, color=color, point=point, line=line)

        self.y2_data = y2_data
