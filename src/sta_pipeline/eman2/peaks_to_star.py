from pathlib import Path
import numpy as np
import pandas as pd
import starfile

from ..utils import *


def peaks_to_star(
    peaks_dataframe: pd.DataFrame,
    output_star: Path,
    tomo_bin_factor: int,
) -> None:
    """Convert a DataFrame of peak coordinates to a star file."""

    output_star = Path(output_star).absolute()

    rln_coordinates = ["rlnCoordinateZ", "rlnCoordinateY", "rlnCoordinateX"]
    rln_angles = ["rlnAngleRot", "rlnAngleTilt", "rlnAnglePsi"]


    peaks_dataframe.rename(columns={'x' : 'rlnCoordinateX', 'y' : 'rlnCoordinateY', 'z' : 'rlnCoordinateZ'}, inplace=True)
    unbinned_peaks_dataframe = peaks_dataframe.copy()
    unbinned_peaks_dataframe[rln_coordinates] = peaks_dataframe[rln_coordinates] * tomo_bin_factor

    for angle in rln_angles:
        random_angles = np.random.randint(0, 179, size=len(unbinned_peaks_dataframe.index))
        unbinned_peaks_dataframe[angle] = random_angles
    
    starfile.write(unbinned_peaks_datafram, output_star, overwrite=True) 
    