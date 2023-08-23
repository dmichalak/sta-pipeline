import subprocess
from pathlib import Path
from typing import Optional
from ..utilities.utils import *

import pandas as pd
import starfile
import mrcfile

from .get_peak_coordinates import get_peak_coordinates
from .peaks_to_star import peaks_to_star


def eman2_extract(
    segmentation_directory: Path,
    neural_network: Path,
    tomo_bin_factor: int,
    min_distance: int,
    border_size: int,
    rel_threshold: float,
    abs_threshold: float,
    concatenate_star_files: bool,
) -> None:
    """Extract peaks from segmentations in EMAN2 directory."""

    segmentation_directory = Path(segmentation_directory).absolute()
    neural_network = Path(neural_network).absolute()
    segment_str = neural_network.stem.split("__")[1]

    peaks_list = []
    ts_dict = {}
    # Convert segmentation maps from .hdf to .mrc
    for hdf in sorted(segmentation_directory.glob("*.hdf")):
        if not hdf.with_suffix(".mrc").exists():
            print(f"Converting {hdf.name} to .mrc...")
            command = [
                "e2proc3d.py",
                str(hdf),
                str(hdf.with_suffix(".mrc")),
            ]
            subprocess.run(command)
        # add ts info to dict
        ts_name = hdf.stem
        ts_dict[ts_name]["tomo_path"] = hdf.with_suffix(".mrc").absolute()

        segment_path = segmentation_directory / f"{ts_name}_{segment_str}.hdf"

        if not segment_path.with_suffix(".mrc").exists():
            print(f"Converting {segment_path.name} to .mrc...")
            command = [
                "e2proc3d.py",
                str(segment_path),
                str(segment_path.with_suffix(".mrc")),
            ]
            subprocess.run(command)
        # add ts info to dict
        ts_dict[ts_name]["segment_path"] = segment_path.with_suffix(".mrc").absolute()

    # Extract peaks from segmentation maps and save to a star file per tomogram
    for ts_name in ts_dict.keys():
        print(f"Loading {ts_name} data...")
        #tomogram_mrc = mrcfile.read(ts_dict[ts_name]["tomo_path"])
        segment_mrc = mrcfile.read(ts_dict[ts_name]["segment_path"])
        starfile_name = f"{segment_mrc.stem}_abs{abs_threshold}rel{rel_threshold}.star"
        if (segmentation_directory / starfile_name).exists():
            print(f"Found {starfile_name}, skipping...")
            continue
        print(f"Extracting peaks from {ts_name}...")
        map_peaks_df = get_peak_coordinates(
            segment_mrc,
            int(min_distance),
            float(rel_threshold),
            float(abs_threshold),
            int(border_size),
        )
        print("Found", len(map_peaks_df.index), "peaks.")
        print(f"Saving peaks to {starfile_name}...")
        peaks_to_star(
            map_peaks_df,
            segmentation_directory / f"{starfile_name}",
            tomo_bin_factor=tomo_bin_factor,
            )
        peaks_list.append(map_peaks_df)

    # Concatenate all star files into one star file
    if concatenate_star_files:
        print("Concatenating all star files...")
        starfile_name = f"particles_abs{abs_threshold}rel{rel_threshold}.star"
        all_peaks = pd.concat(peaks_list, axis=0, ignore_index=True)
        peaks_to_star(
            all_peaks,
            segmentation_directory / starfile_name,
            tomo_bin_factor=tomo_bin_factor,
        )
        print(f"Saved concatenated star file to {segmentation_directory / starfile_name}.")

    print("Done!")
