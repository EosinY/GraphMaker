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
    Linear = "linear"
    Log = "log"

    def Value(e):
        return e.value

    def ToEnum(e: str):
        if e == "1":
            return AxisType.Linear
        elif e == "2":
            return AxisType.Log


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


class GraphMaker():
    entries_xy: list[XY_PlotEntry]
    entries_xy2: list[XY2_PlotEntry]

    _grid: tuple[bool] = (True, True, False)
    _margin: tuple[float] = (0.125, 0.875, 0.125, 0.9)

    def __init__(self, path: str):
        self.path = path

    def _Str2AxisType(i: int) -> Union[tuple[AxisType, AxisType], tuple[AxisType, AxisType, AxisType]]:
        al = []
        for s in str(i):
            al.append(AxisType.ToEnum(s))

        return tuple(al)

    def Plot_XY(
            self,
            axisname: tuple[str, str],
            x_region: tuple[float, float] = (None, None),
            y_region: tuple[float, float] = (None, None),
            axistype: Union[int, tuple[AxisType, AxisType]] = 11,
            ticks: Union[list[float], list[Dict[float, str]]] = None,
            legposition=None):

        return

    def Plot_XY2(
            self,
            axisname: tuple[str, str, str],
            x_region: tuple[float, float] = (None, None),
            y_region: tuple[float, float] = (None, None),
            y2_region: tuple[float, float] = (None, None),
            axistype: Union[int, tuple[AxisType, AxisType, AxisType]] = 111,
            ticks: Union[list[float], list[Dict[float, str]]] = None,
            legposition=None):
        return
