from pathlib import Path
import pandas as pd
from skimage.feature import peak_local_max
import mrcfile



def get_peak_coordinates(
    segment_map: Path,
    min_distance: int,
    threshold_abs: float,
    threshold_rel: float,
    border_size: int
) -> pd.DataFrame:
    """Get the coordinates of the peaks in a segment map. If both threshold_abs and threshold_rel are provided, the maximum of the two is chosen as the minimum intensity threshold of peaks."""

    peaks = peak_local_max(
        mrcfile.read(segment_map),
        min_distance=min_distance,
        threshold_abs=threshold_abs,
        threshold_rel=threshold_rel,
        exclude_border=border_size,
    )

    peaks_df = pd.DataFrame(peaks, columns=["rlnCoordinateZ", "rlnCoordinateY", "rlnCoordinateX"])


    return peaks_df