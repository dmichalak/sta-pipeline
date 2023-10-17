import subprocess
from pathlib import Path
from ..utilities.utils import *

import json
import pandas as pd
import numpy as np
import starfile



def eman2_box_extract(
    eman2_directory: Path,
    tomo_bin_factor: int,
    box_size : int,
    feature_name : str,
    density_threshold : float,
    mass_threshold : float,
) -> None:
    """Extract peaks from segmentations in EMAN2 directory."""
    eman2_directory = Path(eman2_directory).absolute()
    tomogram_directory = eman2_directory / "tomograms"
    segmentation_directory = eman2_directory / "segmentations"
    info_directory = eman2_directory / "info"

    peaks_list = []
    ts_dict = {}
    for hdf in sorted(tomogram_directory.glob("*.hdf")):
        # add ts info to dict
        ts_name = hdf.stem
        ts_dict[ts_name] = {}
        ts_dict[ts_name]["tomogram_path"] = hdf
        ts_dict[ts_name]["segment_path"] = [seg for seg in sorted(segmentation_directory.glob(f"{ts_name}__*.hdf"))][0]

    # Extract peaks from segmentation maps and save to a star file per tomogram
    for ts_name in ts_dict.keys():
        print(f"Extracting peaks from {ts_name}...")
        command = [
            "e2spt_extractfromseg.py",
            f"{ts_dict[ts_name]['tomogram_path']}",
            f"{ts_dict[ts_name]['segment_path']}",
            f"--thresh={density_threshold}",
            f"--featurename={feature_name}",
            f"--boxsz={box_size}",
            "--random=-1",
            f"--massthresh={mass_threshold}",
            "--edge=4",
            "--sort",
        ]
        result = subprocess.run(command)

        ts_json = info_directory / f"{ts_name}_info.json"
        particle_data = json.load(open(ts_json))

        #box_class_map = {}
        #for key in particle_data["class_list"].keys():
        #    box_class_map[str(key)] = particle_data["class_list"][key]["name"]

        particle_df = pd.DataFrame(particle_data["boxes_3d"], columns=["rlnCoordinateX","rlnCoordinateY","rlnCoordinateZ","","",""]).drop(columns="")
        print("Found", len(particle_df.index), "peaks.")
        #particle_df["box_class"] = particle_df["box_class"].astype(str).map(box_class_map)
        particle_df["rlnCoordinateX"] = particle_df["rlnCoordinateX"] - 10
        for coord in ["rlnCoordinateX", "rlnCoordinateY", "rlnCoordinateZ"]:
            particle_df[coord] = particle_df[coord].astype(float) * float(tomo_bin_factor)

        rln_angles = ["rlnAngleRot","rlnAngleTilt","rlnAnglePsi"]
        for angle in rln_angles:
            random_angles = np.random.randint(0,179, size=len(particle_df.index))
            particle_df[angle] = random_angles
        
        particle_df["rlnTomoName"] = ts_name[:6]
        starfile_path = info_directory / f"{ts_name}.star"
        print(f"Saving peaks to {starfile_path}...")
        starfile.write(particle_df, starfile_path, overwrite=True)




    print("Done!")
