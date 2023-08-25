from pathlib import Path
from typing import Optional
from collections import OrderedDict
import re
import sys

import numpy as np
import pandas as pd

from eulerangles import convert_eulers
import starfile
import dynamotable

# based on https://github.com/EuanPyle/dynamo2relion

def convert_tbl2star(
        input_directory: Path,
        input_binning: int,
        ts_directories: Path,
        overwrite: Optional[bool] = False,
):
    input_directory = Path(input_directory).absolute()
    output_directory = input_directory

    for tbl_file in sorted(input_directory.glob("*.tbl")):
        tbl_filename = tbl_file.stem

        tbl_df = dynamotable.read(tbl_file)

        # Initialize a relion dictionary
        relion_dict = {}

        # Get coordinate info from the input tbl file
        for coord in ("x", "y", "z"):
            rln_coord_column = f"rlnCoordinate{coord.upper()}"
            dynamo_shift_column = f"d{coord}"
            relion_dict[rln_coord_column] = (tbl_df[coord] * float(input_binning))

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
	
    	# assign tomo_name to correct particles
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
        

