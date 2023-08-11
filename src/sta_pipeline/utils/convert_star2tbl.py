from pathlib import Path
from typing import Optional
from collections import OrderedDict

import numpy as np
import pandas as pd

from eulerangles import convert_eulers
import starfile
import dynamotable

# based on https://github.com/EuanPyle/relion2dynamo

def convert_star2tbl(
        input_directory: Path,
        input_binning: int,
        output_binning: int,
        overwrite: Optional[bool] = False,
):
    input_directory = Path(input_directory).absolute()
    output_directory = input_directory

    for star_file in sorted(input_directory.glob("*.star")):
        star_filename = star_file.stem

        star_df = starfile.read(star_file)

        if isinstance(star_df, OrderedDict):
            try:
                rln_particles_df = star_df["particles"]
                optics_df = star_df["optics"]
            except KeyError:
                raise RuntimeError("Cannot find data_particles or data_optincs in the star file.")
            
        # Initialize a dynamo dictionary
        dynamo_dict = {} 
        binned_dynamo_dict = {}

        # Get coordinate info from the input star file
        unbinned_pixel_size = optics_df["rlnTomoTiltSeriesPixelSize"][0]

        for coord in ("x", "y", "z"):
            rln_coord_column = f"rlnCoordinate{coord.upper()}"
            rln_shift_column = f"rlnOrigin{coord.upper()}Angst"
            rln_shift = rln_particles_df[rln_shift_column] / unbinned_pixel_size
            # Dynamo coordinates = RELION coordinates - RELION shift
            dynamo_dict[coord] = rln_particles_df[rln_coord_column] - rln_shift
            binned_dynamo_dict[coord] = dynamo_dict[coord] / output_binning

        # Get orientational info from the input star file
        rln_angle_columns = ["rlnAngleRot", "rlnAngleTilt", "rlnAnglePsi"]

        # if rlnAngleRot is not in particles_df
        if not rln_angle_columns[0] in rln_particles_df.columns:
            for angle in rln_angle_columns:
                random_angles = np.random.randint(0,179,size=len(rln_particles_df.index))
                rln_particles_df[angle] = random_angles

        rln_angles = rln_particles_df[rln_angle_columns].to_numpy()
        dynamo_angles = convert_eulers(
            rln_angles,
            source_meta="relion",
            target_meta="dynamo",
        )
        dynamo_dict["tdrot"] = dynamo_angles[:, 0]
        dynamo_dict["tilt"] = dynamo_angles[:, 1]
        dynamo_dict["narot"] = dynamo_angles[:, 2]
        binned_dynamo_dict["tdrot"] = dynamo_dict["tdrot"]
        binned_dynamo_dict["tilt"] = dynamo_dict["tilt"]
        binned_dynamo_dict["narot"] = dynamo_dict["narot"]

        # Get tomogram info from the input star file
        dynamo_dict["tomo"] = rln_particles_df["rlnTomoName"].str.split("_").str[1]
        binned_dynamo_dict["tomo"] = dynamo_dict["tomo"]

        if "rlnObjectNumber" in rln_particles_df.columns:
            dynamo_dict["reg"] = rln_particles_df["rlnObjectNumber"]
            binned_dynamo_dict["reg"] = dynamo_dict["reg"]

        if "rlnClassNumber" in rln_particles_df.columns:
            dynamo_dict["class"] = rln_particles_df["rlnClassNumber"]
            binned_dynamo_dict["class"] = dynamo_dict["class"]
        
        dynamo_df = pd.DataFrame.from_dict(dynamo_dict)
        binned_dynamo_df = pd.DataFrame.from_dict(binned_dynamo_dict)

        # Write the dynamo table
        dynamotable.write(dynamo_df, output_directory / f"{star_filename}_unb.tbl")
        dynamotable.write(binned_dynamo_df, output_directory /  f"{star_filename}_b{output_binning}.tbl")
        

