from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

from eulerangles import convert_eulers
import starfile
import dynamotable

# based on https://github.com/EuanPyle/dynamo2relion

def convert_tbl2star(
        input_tbl_file: Path,
        input_binning: int,
        ts_directories: Path,
        overwrite: Optional[bool] = False,
):
    input_tbl_file = Path(input_tbl_file).absolute()
    output_directory = input_tbl_file.parent

    tbl_filename = input_tbl_file.stem

    tbl_df = dynamotable.read(input_tbl_file)

    # Initialize a relion dictionary
    relion_dict = {}

    # Get coordinate info from the input tbl file
    for coord in ("x", "y", "z"):
        rln_coord_column = f"rlnCoordinate{coord.upper()}"
        dynamo_shift_column = f"d{coord}"
        # rln coordinate = (dynamo coordinate + dynamo shift) * input_binning
        relion_dict[rln_coord_column] = (tbl_df[coord] + tbl_df[dynamo_shift_column]) * float(input_binning)

    # Get orientational info from the input tbl file
    dynamo_angles = tbl_df[["tdrot", "tilt", "narot"]].to_numpy()
    warp_angles = convert_eulers(
        dynamo_angles,
        source_meta="dynamo",
        target_meta="warp",
    )
    rln_angle_columns = ["rlnAngleRot", "rlnAngleTilt", "rlnAnglePsi"]
    relion_dict[rln_angle_columns[0]] = warp_angles[:, 0]
    relion_dict[rln_angle_columns[1]] = warp_angles[:, 1]
    relion_dict[rln_angle_columns[2]] = warp_angles[:, 2]

    # Get tomogram info from the input tbl file
    dynamo_tomo_index = tbl_df["tomo"].to_numpy()
#    print(dynamo_tomo_index)

    ts_list = []
    for ts_dir in sorted(ts_directories.glob("*_*")):
        if ts_dir.is_dir():
            ts_list.append(ts_dir.stem)
    tomo_name_list = [''] * len(dynamo_tomo_index)

    #####
    # From github.com/EuanPyle/dynamo2relion in _utils.py
    tomo_index = 1
    for tomo_name in ts_list:
        tomo_num = tomo_index
	
    # Assign tomo_name to correct particles
        tomo_name_indices = np.asarray(np.where(dynamo_tomo_index == tomo_num))[0]

        for i in tomo_name_indices:
            tomo_name_list[i] = tomo_name
        tomo_index += 1
    #####

    relion_dict["rlnTomoName"] = tomo_name_list
    # Label the particles with unique object numbers
    relion_dict["rlnObjectNumber"] = np.arange(len(tbl_df.index)) + 1

    relion_df = pd.DataFrame.from_dict(relion_dict)

    # Write the relion star file
    relion_star_file = output_directory / f"{tbl_filename}.star"
    starfile.write(relion_df, relion_star_file, overwrite=overwrite)
    print(f"Wrote {relion_star_file}")

    return
        

