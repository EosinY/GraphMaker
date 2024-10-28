import matplotlib.pyplot as plt
from typing import Final, Union, Dict, List, Tuple
from enum import Enum, unique

import Colors
import Legend


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
            line: Union[LineType, tuple[LineType, float]] = (LineType.Solid, 1.5),
            disable: bool = False):

        self.x_data = x_data
        self.y_data = y_data
        self.name = name

        self.groupid = groupid

        self.disable = disable

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
            self.linewidth = line[1]


class XY2_PlotEntry(XY_PlotEntry):
    def __init__(self, x_data, y_data, y2_data, name, *, groupid=None, color=None, point=(PointType.Circle, 1), line=(LineType.Solid, 1.5), disable):
        super().__init__(x_data, y_data, name, groupid=groupid, color=color, point=point, line=line, disable=disable)

        self.y2_data = y2_data


class GraphMaker():
    entries_xy: list[XY_PlotEntry]
    entries_xy2: list[XY2_PlotEntry]

    _grid: tuple[bool] = (True, False)
    _margin: tuple[float] = (0.125, 0.875, 0.125, 0.9)
    _colorscm: List[str] = Colors.gnuplot_colors_1

    _fig = plt.figure()
    _ax1 = _fig.add_subplot(111)
    _ax2 = _ax1.twinx()
    _leg = [(_ax1.get_legend_handles_labels()), (_ax2.get_legend_handles_labels())]

    def __init__(self, path: str):
        self.path = path

    def _Int2AxisType(i: int, l: int) -> Union[tuple[AxisType, AxisType], tuple[AxisType, AxisType, AxisType]]:
        al = []
        s = str(i)
        if len(s) < l:
            raise TypeError("axes type defining int digit is shorter than desired.")

        for j in range(l):
            al.append(s[j])

        return tuple(al)

    def _GetColor(self, ent: Union[List[XY_PlotEntry], List[XY2_PlotEntry]], idx: int) -> str:
        if ent[idx].color is not None:
            return ent[idx].color
        elif ent[idx].color is None and idx == 0:
            return self._colorscm[0]
        elif (ent[idx].color is None and ent[idx - 1].color is None) and idx > 0:
            i = idx if idx < len(self._colorscm) else idx % len(self._colorscm)
            return self._colorscm[i]
        elif (ent[idx].groupid == ent[idx - 1].groupid) and idx > 0:
            return ent[idx - 1].color
        else:
            raise ("are you serious? my brain is gonna crash into fucking cream bruh(by me coding @2:30am)")

    def _SetXLimit(ax: plt.Axes, lower: float, upper: float) -> None:
        if upper is not None:
            ax.set_xlim(left=upper)
        if lower is not None:
            ax.set_xlim(right=lower)

    def _SetYLimit(ax: plt.Axes, lower: float, upper: float) -> None:
        if upper is not None:
            ax.set_ylim(top=upper)
        if lower is not None:
            ax.set_ylim(bottom=lower)

    def _SetManXTicks(ax: plt.Axes, xticks: Union[List[float], Dict[float, str]]):
        if xticks is None:
            return

        if xticks is list[float]:
            ax.set_xticks(xticks)
        else:
            ax.set_xticks(list(xticks.keys()))
            ax.set_xticklabels(list(xticks.values()))

    def _SetManYTicks(ax: plt.Axes, yticks: Union[List[float], Dict[float, str]]):
        if yticks is None:
            return

        if yticks is list[float]:
            ax.set_yticks(yticks)
        else:
            ax.set_yticks(list(yticks.keys()))
            ax.set_yticklabels(list(yticks.values()))

    def AddEntry(self, entry: Union[XY_PlotEntry, XY2_PlotEntry]) -> None:
        if entry is XY_PlotEntry:
            self.entries_xy.append(entry)
        elif entry is XY2_PlotEntry:
            self.entries_xy2.append(entry)

    def Plot_XY(
            self,
            axisname: tuple[str, str],
            axistype: Union[int, tuple[AxisType, AxisType]] = 11,
            x_region: tuple[float, float] = (None, None),
            y_region: tuple[float, float] = (None, None),
            x_ticks: Union[list[float], list[Dict[float, str]]] = None,
            y_ticks: Union[list[float], list[Dict[float, str]]] = None,
            legposition: Legend.Position = Legend.Position.Best) -> None:

        i: int = 0
        for e in self.entries_xy:
            if e.disable:
                continue

            show_legend = False
            color = self._GetColor(e.color, e.groupid, i)
            if e.name is None:
                self._ax1.plot(e.x_data, e.y_data, color=color, marker=e.pointtype, markersize=e.pointsize, linestyle=e.linetype, linewidth=e.linewidth)
            else:
                self._ax1.plot(e.x_data, e.y_data, label=e.name, color=color, marker=e.pointtype, markersize=e.pointsize, linestyle=e.linetype, linewidth=e.linewidth)
                show_legend = True

            # Axis Settings
            self._ax1.grid(self._grid[0])
            axtype = self._Int2AxisType(axistype, 2) if axistype is int else axistype
            self._ax1.set_xscale(axtype[0].Value())
            self._ax1.set_yscale(axtype[1].Value())

            plt.subplots_adjust(left=self._margin[0], right=self._margin[1], bottom=self._margin[2], top=self._margin[3])

            # Legend
            if show_legend:
                le = Legend.Legend()
                le.set_legend(self._ax1, self._leg[0][0], self._leg[0][1], legposition)

            # Plotting Limit
            self._SetXLimit(self._ax1, x_region[0], x_region[1])
            self._SetYLimit(self._ax1, y_region[0], y_region[1])

            # Ticks
            self._SetManXTicks(self._ax1, x_ticks)
            self._SetManYTicks(self._ax1, y_ticks)

            # Label
            self._ax1.set_xlabel(axisname[0])
            self._ax1.set_ylabel(axisname[1])

            i += 1
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
