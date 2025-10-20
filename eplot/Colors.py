from typing import Final, List

gnuplot_colors_1: Final[List[str]] = [
    "#9400d3",
    "#008b8b",
    "#87ceeb",
    "#daa520",
    "#ffd700",
    "#4169e1",
    "#8b0000"
]
gnuplot_colors_2: Final[List[str]] = [
    "#daa520",
    "#87ceeb",
    "#008b8b",
    "#ff8c00",
    "#4169e1",
    "#b8860b",
    "#ffa500"
]
universal_colors: Final[List[str]] = [
    "#FF4B00",
    "#005AFF",
    "#03AF7A",
    "#4DC4FF",
    "#F6AA00",
    "#D50AB0",
    "#101010"
]
muted_colors: Final[List[str]] = [
    "#332288",
    "#88CCEE",
    "#44AA99",
    "#117733",
    "#999933",
    "#DDCC77",
    "#CC6677",
    "#882255",
    "#AA4499",
    "#DDDDDD"
]


def get_color_variant(color_l: list[str], num: int, start: int = 0, stop: int = -1, mlt_val: tuple[float, float, float] = (0.8, 0.8, 0.8)):
    color_l = color_l[start:stop]
    mcolor_l = []

    color_nums = [int(s.lstrip("#"), 16) for s in color_l]
    mask_shifts = [16, 8, 0]
    for color in color_nums:
        color_rgb = [(color & (0xFF << i)) >> i for i in mask_shifts]
        mod_clrgb = [int(color_rgb[i] * (mlt_val[i] / num)) for i in range(len(color_rgb))]
        mcolor = 0
        for i in range(len(mod_clrgb)):
            c = mod_clrgb[i]
            mcolor |= c << mask_shifts[i]

        mcolor_l.append("#" + "{:06x}".format(mcolor))

    return mcolor_l
