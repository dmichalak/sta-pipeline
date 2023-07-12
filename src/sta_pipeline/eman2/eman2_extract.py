from pathlib import Path
import pandas as pd
from typing import Optional
from ..utils import *

from .get_peak_coordinates import get_peak_coordinates
from .peaks_to_star import peaks_to_star


def eman2_extract(
    eman2_directory: Path,
    min_distance: int,
    rel_threshold: float,
    abs_threshold: float,
) -> None:
    peaks_list = []
    for segment_map in eman2_directory.glob("segmentations/*.mrc"):
        map_peaks_df = get_peak_coordinates(segment_map, min_distance, rel_threshold, abs_threshold)
        peaks_list.append(map_peaks_df)
    peaks_df = pd.concat(peaks_list, axis=1, ignore_index=True) 
    peaks_to_star(peaks_df, segment_map.with_suffix(".star"), 1)