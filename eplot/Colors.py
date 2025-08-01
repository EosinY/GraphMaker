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


def get_color_variant(color_l: list[str], count: int, start: int = 0, sub_val: tuple[int, int, int] = (0x30, 0x30, 0x30)):
    color_l = color_l[start:count]
    mcolor_l = []

    color_nums = [int(s.lstrip("#"), 16) for s in color_l]
    mask_shifts = [16, 8, 0]
    for color in color_nums:
        color_rgb = [(color & (0xFF << i)) >> i for i in mask_shifts]
        mod_clrgb = [color_rgb[i] - sub_val[i] if color_rgb[i] - sub_val[i] >= 0 else 0 for i in range(len(color_rgb))]
        mcolor = 0
        for i in range(len(mod_clrgb)):
            c = mod_clrgb[i]
            mcolor |= c << mask_shifts[i]

        mcolor_l.append("#" + hex(mcolor).lstrip("0x"))

    return color_l + mcolor_l
