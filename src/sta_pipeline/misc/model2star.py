from pathlib import Path
import pandas as pd
import numpy as np

import imodmodel
import starfile

# This script converts a set of IMOD model files (.mod) into a set of STAR files (.star) that can be used as a particle coordinate file in RELION-4.0. 
# This script assumes the names of the model files are the same as the names of the tomograms they were extracted from.


# Set the following variables
path_to_model_directory = "/data/singal/cryo-ET-recon/models" # Path to the directory containing the models (in .mod format)
randomize_particle_angles = True # If True, randomize the angles of the particles. If False, set all angles to 0.0







#######################
# Do not change anything below this line
#######################

# Read all model files in the directory and store them in a dictionary
path_to_model_directory = Path(path_to_model_directory).absolute() 
model_dict = {}
for model in path_to_model_directory.glob("*.mod"):
    if model.stem in model_dict.keys():
        raise ValueError("Multiple model files with the same name found in the directory: ", path_to_model_directory)
    else: 
        model_dict[model.stem] = imodmodel.read(model)
        model_dict[model.stem]["name"] = model.stem

# Check if any models were found at path_to_model_directory
if len(model_dict) == 0:
    raise ValueError("No model files found in the directory: ", path_to_model_directory)
else:
    # Create a star file for each model file
    star_dict = {}

    for key in list(model_dict.keys()):
        star_dict[key] = pd.DataFrame()
        star_dict[key]["rlnTomoName"] = model_dict[key]["name"]
        star_dict[key]["rlnCoordinateX"] = model_dict[key]["x"]
        star_dict[key]["rlnCoordinateY"] = model_dict[key]["y"]
        star_dict[key]["rlnCoordinateZ"] = model_dict[key]["z"]

        # Set the angles of the particles
        if randomize_particle_angles == True:
            star_dict[key]["rlnAngleRot"] = np.random.uniform(0, 180, len(model_dict[key]))
            star_dict[key]["rlnAngleTilt"] = np.random.uniform(0,180, len(model_dict[key]))
            star_dict[key]["rlnAnglePsi"] = np.random.uniform(0, 180, len(model_dict[key]))
        else:
            star_dict[key]["rlnAngleRot"] = 0.0
            star_dict[key]["rlnAngleTilt"] = 0.0
            star_dict[key]["rlnAnglePsi"] = 0.0 

    # Write the star files for each model found in the directory
    for key in star_dict.keys():
        starfile.write(star_dict[key], path_to_model_directory / f"{star_dict[key]['rlnTomoName'][0]}.star", overwrite=True)
        print("Star file written at: ", path_to_model_directory / f"{star_dict[key]['rlnTomoName'][0]}.star")
    
    print("Done!")