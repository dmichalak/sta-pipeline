from pathlib import Path
import numpy as np
import pandas as pd
import starfile

from ..utilities.utils import *


def peaks_to_star(
    peaks_dataframe: pd.DataFrame,
    output_star: Path,
    tomo_bin_factor: int,
) -> None:
    """Convert a DataFrame of peak coordinates to a star file."""

    output_star = Path(output_star).absolute()

    rln_coordinates = ["rlnCoordinateZ", "rlnCoordinateY", "rlnCoordinateX"]
    rln_angles = ["rlnAngleRot", "rlnAngleTilt", "rlnAnglePsi"]
    optics_columns = ["rlnOpticsGroup", "rlnOpticsGroupName", "rlnVoltage", "rlnSphericalAberration", "rlnTomoTiltSeriesPixelSize"]
    optics_values = [1, "opticsGroup1", 300, 2.7, 1.0825]
    peaks_dataframe.rename(
        columns={"x": "rlnCoordinateX", "y": "rlnCoordinateY", "z": "rlnCoordinateZ"},
        inplace=True,
    )
    unbinned_peaks_dataframe = {}
    unbinned_peaks_dataframe["optics"] = pd.DataFrame(columns=optics_columns)
    unbinned_peaks_dataframe["optics"].loc[0] = optics_values

    unbinned_peaks_dataframe["particles"][rln_coordinates] = (
        peaks_dataframe[rln_coordinates] * tomo_bin_factor
    )

    for angle in rln_angles:
        random_angles = np.random.randint(
            0, 179, size=len(unbinned_peaks_dataframe.index)
        )
        unbinned_peaks_dataframe["particles"][angle] = random_angles
    # if rlnTomoName is a column in peaks_dataframe, move it to the last column index
    if "rlnTomoName" in peaks_dataframe.columns:
        unbinned_peaks_dataframe["particles"]["rlnTomoName"] = peaks_dataframe["rlnTomoName"]
        unbinned_peaks_dataframe["particles"] = unbinned_peaks_dataframe["particles"][
            [
                col
                for col in unbinned_peaks_dataframe["particles"].columns
                if col != "rlnTomoName"
            ]
            + ["rlnTomoName"]
        ]
    unbinned_peaks_dataframe["particles"]["rlnOpticsGroup"] = 1
    unbinned_peaks_dataframe["particles"]["rlnOriginXAngst"] = 0.0
    unbinned_peaks_dataframe["particles"]["rlnOriginYAngst"] = 0.0
    unbinned_peaks_dataframe["particles"]["rlnOriginZAngst"] = 0.0

    starfile.write(unbinned_peaks_dataframe, output_star, overwrite=True)
