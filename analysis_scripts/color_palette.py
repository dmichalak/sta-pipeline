
def color_palette(
        palette: str = "default",
) -> list:
    """
    Return a list of colors for plotting.
    """
    contrast_three = ["#004388", "#ba5566", "#ddaa33"]
    zesty_four = ["#0f2080", "#f5793b", "#a95aa1", "#85c0f9"]
    ito_seven = ["#0070ae", "#d55e00", "#009e72", "#cb78a7", "#56b4e9", "#e79f02", "#f1e443"]
    if palette == "default":
        return ito_seven
    elif palette == "contrast_three":
        return contrast_three
    elif palette == "zesty_four":
        return zesty_four
    elif palette == "ito_seven":
        return ito_seven
    else:
        raise ValueError(f"Palette {palette} not recognized.")