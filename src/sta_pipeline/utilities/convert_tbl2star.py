from pathlib import Path
from typing import Optional
import re
import sys

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
    dynamo_tomoname = tbl_df["tomo"].to_numpy()

    ts_list = []
    for ts_dir in ts_directories.glob("*_*"):
        if ts_dir.is_dir():
            ts_list.append(ts_dir.stem)
    tomo_name_list = [''] * len(dynamo_tomoname)

    #####
    # From github.com/EuanPyle/dynamo2relion in _utils.py
    for tomo_name in ts_list:
        ts_string=re.split('(\d+)',tomo_name)
        while('' in ts_string) :
            ts_string.remove('')
        if len(ts_string) > 2:
            sys.exit('Check the folder names in tilt_series_directory. Should only contain folders with variations of the ts_01 TS_15 etc. naming convention')
        tomo_num = int(ts_string[1])
	
    # Assign tomo_name to correct particles
        tomo_name_indices = np.asarray(np.where(dynamo_tomoname == tomo_num))[0]

        for i in tomo_name_indices:
            tomo_name_list[i] = tomo_name
    #####

    relion_dict["rlnTomoName"] = tomo_name_list
    # Label the particles with unique object numbers
    relion_dict["rlnObjectNumber"] = np.arange(len(dynamo_tomoname)) + 1

    relion_df = pd.DataFrame.from_dict(relion_dict)

    # Write the relion star file
    relion_star_file = output_directory / f"{tbl_filename}.star"
    starfile.write(relion_df, relion_star_file, overwrite=overwrite)
    print(f"Wrote {relion_star_file}")

    return
        
