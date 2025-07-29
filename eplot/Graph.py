import matplotlib.pyplot as plt
from typing import Final, Union, Dict, List, Tuple
from enum import Enum, Flag, auto, unique
import numpy as np
from matplotlib.axes import Axes

from . import Colors
from . import Legend


@unique
class Switches(Flag):
    Blank = auto()
    Square_XY = auto()
    Square_XY2 = auto()
    DoNotSave = auto()
    Square = Square_XY | Square_XY2


@unique
class PointType(Enum):
    Dot = "."
    Circle = "o"
    UpTriangle = "^"
    DownTriangle = "v"
    Square = "s"
    Cross = "x"
    Plus = "+"
    Blank = ""

    def Value(e):
        return e.value


@unique
class LineType(Enum):
    Solid = "-"
    Dash = "--"
    DashDot = "-."
    Dot = ":"
    Blank = ""

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


class XY_PlotEntry(object):
    def __init__(
            self,
            x_data: list[float], y_data: list[float], name: str, *,
            groupid: str = None, color: str = None,
            point: Union[PointType, tuple[PointType, float]] = None,
            line: Union[LineType, tuple[LineType, float]] = None,
            disable: bool = False):

        self.x_data = x_data
        self.y_data = y_data
        self.name = name

        self.groupid = groupid

        self.disable = disable

        self.color = color
        self.pointtype = PointType.Blank if point is None and line is not None else PointType.Circle
        self.pointsize = 4
        if isinstance(point, PointType):
            self.pointtype = self.pointtype.value if point is None else point.value
        else:
            self.pointtype = self.pointtype.value if point is None else point[0].value
            self.pointsize = self.pointsize if point is None else point[1]

        self.linetype = LineType.Blank if line is None and point is not None else LineType.Solid
        self.linewidth = 1.5
        if isinstance(line, LineType):
            self.linetype = self.linetype.value if line is None else line.value
        else:
            self.linetype = self.linetype.value if line is None else line[0].value
            self.linewidth = self.linewidth if line is None else line[1]


class XY2_PlotEntry(XY_PlotEntry):
    def __init__(
            self,
            x_data: list[float], y2_data: list[float], name: str, *,
            groupid: str = None, color: str = None,
            point: Union[PointType, Tuple[PointType, float]] = None,
            line: Union[LineType, Tuple[LineType, float]] = None,
            disable=False):
        super().__init__(x_data, y2_data, name, groupid=groupid, color=color, point=point, line=line, disable=disable)


class GraphMaker():
    entries_xy: list[XY_PlotEntry] = []
    entries_xy2: list[XY2_PlotEntry] = []

    setings: dict = {}

    # Grid enable (x-y, x-y2)
    _grid: tuple[bool] = (True, False)
    # Graph margin (I think this param will be good)
    _margin: tuple[float] = (0.125, 0.85, 0.125, 0.875)
    # Colorscheme (You can add any schemes by adding list[str] in Colors.py)
    _colorscm: List[str] = Colors.gnuplot_colors_1

    # plot objects (You can access even outside the class to control more (but bad method  should replace with something good ones))
    _fig = None
    _ax1 = None
    _ax2 = None
    _leg_xy = ([], [])
    _leg_xy2 = ([], [])

    def __init__(self, path: str):
        self.path = path
        self.entries_xy = []
        self.entries_xy2 = []

    def _Int2AxisType(self, i: int, l: int) -> Union[tuple[AxisType, AxisType], tuple[AxisType, AxisType, AxisType]]:
        al = []
        s = str(i)
        if len(s) < l:
            raise TypeError("axes type defining int digit is shorter than desired.")

        for j in range(l):
            al.append(AxisType.ToEnum(s[j]))

        return tuple(al)

    def _GetColor(self, ent: Union[List[XY_PlotEntry], List[XY2_PlotEntry]], idx: int) -> str:
        # None -> pick color from defined colorscheme and change one by one
        # same group id -> pick the color that is same previous plot color
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

    def _SetXLimit(self, ax: plt.Axes, lower: float, upper: float) -> None:
        if upper is not None:
            ax.set_xlim(left=upper)
        if lower is not None:
            ax.set_xlim(right=lower)

    def _SetYLimit(self, ax: plt.Axes, lower: float, upper: float) -> None:
        if upper is not None:
            ax.set_ylim(top=upper)
        if lower is not None:
            ax.set_ylim(bottom=lower)

    def _SetManXTicks(self, ax: plt.Axes, xticks: Union[List[float], Dict[float, str]]):
        if xticks is None:
            return

        if isinstance(xticks, list):
            ax.set_xticks(xticks)
        else:
            ax.set_xticks(list(xticks.keys()))
            ax.set_xticklabels(list(xticks.values()))

    def _SetManYTicks(self, ax: plt.Axes, yticks: Union[List[float], Dict[float, str]]):
        if yticks is None:
            return

        if isinstance(yticks, list):
            ax.set_yticks(yticks)
        else:
            ax.set_yticks(list(yticks.keys()))
            ax.set_yticklabels(list(yticks.values()))

    def AddEntry(self, entry: Union[XY_PlotEntry, XY2_PlotEntry]) -> None:
        if entry.__class__.__name__ == XY_PlotEntry.__name__:
            self.entries_xy.append(entry)
        elif entry.__class__.__name__ == XY2_PlotEntry.__name__:
            self.entries_xy2.append(entry)

    def Plot(
            self,
            axisname: Union[tuple[str, str], tuple[str, str, str]] = ("", "", ""),
            axistype: Union[int, tuple[AxisType, AxisType], tuple[AxisType, AxisType, AxisType]] = 111,
            x_region: tuple[float, float] = (None, None),
            y_region: tuple[float, float] = (None, None),
            y2_region: tuple[float, float] = (None, None),
            x_ticks: Union[list[float], list[Dict[float, str]]] = None,
            y_ticks: Union[list[float], list[Dict[float, str]]] = None,
            y2_ticks: Union[list[float], list[Dict[float, str]]] = None,
            legposition: Legend.Position = Legend.Position.Best,
            aspect: list[int] = [6, 6],
            switch: Switches = Switches.Blank,
            path: str = "") -> tuple[Axes, Axes]:

        self._fig = plt.figure(figsize=aspect)

        show_legend = False
        # Plotting x-y axis
        if len(self.entries_xy) > 0:
            self._ax1 = self._fig.add_subplot(111)

            i: int = 0
            show_legend_xy = False
            for e in self.entries_xy:
                if e.disable:
                    continue

                color = self._GetColor(self.entries_xy, i)
                if e.name is None:
                    self._ax1.plot(e.x_data, e.y_data, color=color, marker=e.pointtype, markersize=e.pointsize, linestyle=e.linetype, linewidth=e.linewidth)
                else:
                    self._ax1.plot(e.x_data, e.y_data, label=e.name, color=color, marker=e.pointtype, markersize=e.pointsize, linestyle=e.linetype, linewidth=e.linewidth)
                    show_legend = True
                    show_legend_xy = True

                i += 1

            # Axis Settings
            self._ax1.grid(self._grid[0])
            axtype = self._Int2AxisType(axistype, 2) if isinstance(axistype, int) else axistype
            self._ax1.set_xscale(axtype[0].Value())
            self._ax1.set_yscale(axtype[1].Value())

            # Legend
            if show_legend_xy:
                self._leg_xy = self._ax1.get_legend_handles_labels()

            # Plotting Limit
            self._SetXLimit(self._ax1, x_region[0], x_region[1])
            self._SetYLimit(self._ax1, y_region[0], y_region[1])

            # Ticks
            self._SetManXTicks(self._ax1, x_ticks)
            self._SetManYTicks(self._ax1, y_ticks)

            # Label
            self._ax1.set_xlabel(axisname[0])
            self._ax1.set_ylabel(axisname[1])

            self._ax1.set_aspect("equal" if Switches.Square_XY in switch else "auto")
        else:
            raise TypeError("x-y plotting is needed.")

        # Plotting x-y2 axis
        # it should be used with x-y, not x-y2 alone (_ax2 is need to define _ax1 before, so x-y2 only never works just goes fuck)
        # if you want to plot only x-y2, adding blank XY_PlotEntry to 'entries_xy' will be work??? but there's no worth to do it than just using x-y.
        if len(self.entries_xy2) > 0:
            self._ax2 = self._ax1.twinx()

            i: int = 0
            show_legend_xy2 = False
            for e in self.entries_xy2:
                if e.disable:
                    continue

                color = self._GetColor(self.entries_xy2, i)
                if e.name is None:
                    self._ax2.plot(e.x_data, e.y_data, color=color, marker=e.pointtype, markersize=e.pointsize, linestyle=e.linetype, linewidth=e.linewidth)
                else:
                    self._ax2.plot(e.x_data, e.y_data, label=e.name, color=color, marker=e.pointtype, markersize=e.pointsize, linestyle=e.linetype, linewidth=e.linewidth)
                    show_legend = True
                    show_legend_xy2 = True

                i += 1

            # Axis Settings
            self._ax2.grid(self._grid[1])
            axtype = self._Int2AxisType(axistype, 3) if isinstance(axistype, int) else axistype
            self._ax2.set_yscale(axtype[2].Value())

            # Legend
            if show_legend_xy2:
                self._leg_xy2 = self._ax2.get_legend_handles_labels()

            # Plotting Limit
            self._SetYLimit(self._ax2, y2_region[0], y2_region[1])

            # Ticks
            self._SetManYTicks(self._ax2, y2_ticks)

            # Label
            self._ax2.set_ylabel(axisname[2])

            self._ax2.set_aspect("equal" if Switches.Square_XY2 in switch else "auto")

        if show_legend:
            le = Legend.Legend()
            le.set_legend(self._ax1 if self._ax2 is None else self._ax2, self._leg_xy[0] + self._leg_xy2[0], self._leg_xy[1] + self._leg_xy2[1], legposition, len(self.entries_xy2) > 0)

        self._fig.subplots_adjust(left=self._margin[0], right=self._margin[1], bottom=self._margin[2], top=self._margin[3])

        if Switches.DoNotSave not in switch:
            self._fig.savefig(path if self.path == "" else self.path, bbox_inches='tight')

        return (self._ax1, self._ax2)

    def SaveFig(self, figpath: str = ""):
        path = figpath if len(figpath) > 0 else self.path
        self._fig.savefig(path if self.path == "" else self.path, bbox_inches="tight")
