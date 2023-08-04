import subprocess
from pathlib import Path
from typing import Optional
from ..utils import *

import pandas as pd
import starfile

from .get_peak_coordinates import get_peak_coordinates
from .peaks_to_star import peaks_to_star


def eman2_extract(
    segmentation_directory: Path,
    min_distance: int,
    rel_threshold: float,
    abs_threshold: float,
) -> None:
    """Extract peaks from segmentations in EMAN2 directory."""

    segmentation_directory = Path(segmentation_directory).absolute()

    peaks_list = []
    for hdf in sorted(segmentation_directory.glob("*.hdf")):
        if not hdf.with_suffix(".mrc").exists():
            command = [
                "e2proc3d.py",
                str(hdf),
                str(hdf.with_suffix(".mrc")),
            ]
            subprocess.run(command)
    for segment_map in sorted(segmentation_directory.glob("*.mrc")):
        starfile_name = f"{segment_map.stem}_abs{abs_threshold}rel{rel_threshold}.star"
        if (segmentation_directory / starfile_name).exists():
            print(f"Found {starfile_name}, skipping...")
            continue
        print(f"Extracting peaks from {segment_map.name}...")
        map_peaks_df = get_peak_coordinates(
            segment_map,
            int(min_distance),
            float(rel_threshold),
            float(abs_threshold)
        )
        print("Found", len(map_peaks_df.index), "peaks.")
        print(f"Saving peaks to {starfile_name}...")
        peaks_to_star(
            map_peaks_df,
            segmentation_directory / f"{starfile_name}",
            tomo_bin_factor=1,
            )
        peaks_list.append(map_peaks_df)
    peaks_df = pd.concat(peaks_list, axis=0, ignore_index=True)
    peaks_starfile_name = f"allpeaks_abs{abs_threshold}rel{rel_threshold}.star"
    print(f"Saving all found peaks to {segmentation_directory / (f'{peaks_starfile_name}')}...")
    starfile.write(
        peaks_df,
        segmentation_directory / peaks_starfile_name,
        overwrite=True,
        )
    print("Done!")
