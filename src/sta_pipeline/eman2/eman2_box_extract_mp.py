import subprocess
import time
from pathlib import Path
from multiprocessing import Pool
import json
import pandas as pd
import numpy as np

import starfile

from ..utilities.utils import *

def eman2_box_extract(
    input_data
) -> None:
    """Extract peaks from segmentations in EMAN2 directory."""
    tomogram = input_data[0]
    eman2_directory = input_data[1]
    tomo_bin_factor = input_data[2]
    box_size = input_data[3]
    feature_name = input_data[4]
    density_threshold = input_data[5]
    mass_threshold = input_data[6]

    tomogram_path = tomogram.absolute()
    eman2_directory = eman2_directory.absolute()
    tomogram_directory = eman2_directory / "tomograms"
    segmentation_directory = eman2_directory / "segmentations"
    info_directory = eman2_directory / "info"

    tomogram_name = tomogram.stem
    ts_name = tomogram_name[:6]
    segment_path = [seg for seg in sorted(segmentation_directory.glob(f"{tomogram_name}__*.hdf"))][0]

    # Extract peaks from segmentation maps and save to a star file per tomogram
    print(f"Extracting peaks from {ts_name}...")
    command = [
        "e2spt_extractfromseg.py",
        f"{tomogram_path}",
        f"{segment_path}",
        f"--thresh={density_threshold}",
        f"--featurename={feature_name}",
        f"--boxsz={box_size}",
        "--random=-1",
        f"--massthresh={mass_threshold}",
        "--edge=4",
        "--sort",
    ]
    result = subprocess.run(command)
    


def eman2_box_extract_mp(
    eman2_directory: Path,
    num_processes: int,
    tomo_bin_factor: int,
    box_size : int,
    feature_name : str,
    density_threshold : float,
    mass_threshold : float,
) -> None:
    eman2_directory = Path(eman2_directory).absolute()
    tomogram_directory = eman2_directory / "tomograms"

    data_to_process = []
    #for tomogram in sorted(tomogram_directory.glob("*.hdf")):
    #    data_to_process.append([tomogram, eman2_directory, tomo_bin_factor, box_size, feature_name, density_threshold, mass_threshold])

    #with Pool(processes=int(num_processes)) as pool:
    #    pool.map(eman2_box_extract, data_to_process)

    for ts_json in sorted(eman2_directory.glob("info/*.json")):
        particle_data = json.load(open(ts_json))

        ts_name = ts_json.stem[:6]

        particle_df = pd.DataFrame(particle_data["boxes_3d"], columns=["rlnCoordinateX","rlnCoordinateY","rlnCoordinateZ","","",""]).drop(columns="")
        print("Found", len(particle_df.index), "peaks.")
        particle_df["rlnCoordinateX"] = particle_df["rlnCoordinateX"] - 10
        for coord in ["rlnCoordinateX", "rlnCoordinateY", "rlnCoordinateZ"]:
            particle_df[coord] = particle_df[coord].astype(float) * float(tomo_bin_factor)
        rln_angles = ["rlnAngleRot","rlnAngleTilt","rlnAnglePsi"]
        for angle in rln_angles:
            random_angles = np.random.randint(0,179, size=len(particle_df.index))
            particle_df[angle] = random_angles
    
        particle_df["rlnTomoName"] = ts_name
        starfile_path = eman2_directory / f"info/{ts_name}_particles.star"
        print("Writing ", starfile_path.name, "...")
        starfile.write(particle_df, starfile_path, overwrite=True)



    print("Done!")