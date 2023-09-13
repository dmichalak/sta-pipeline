from pathlib import Path
from typing import Optional

import pandas as pd

import starfile

from .split_classif_star import split_classif_star

def rln_select_good_classes(
        classif_directory : Path,
        good_classes : str,
        overwrite : Optional[bool] = False,
) -> dict:
    """
    Selects the good classes from the class_*.star files, concatenates, and writes them to a new star file.

    Args:
        classif_directory (Path): Path to the directory containing the class_*.star files
        good_classes (str): List of good classes in the format "1,2,3,4,5"
        overwrite (bool): Whether to overwrite existing star files

    Returns:
        good_classes_dict (dict): Dictionary of "particles" and "optics" for each good class
    """

    classif_directory = Path(classif_directory).absolute()

    split_classif_star(classif_directory, overwrite)

    class_star_files = sorted(classif_directory.glob("class*.star"))

    good_classes = [int(x) for x in good_classes.split(",")]

    # Create a dictionary of good and bad classes
    good_classes_dict = {"optics": None, "particles": None}
    bad_classes_dict = {"optics": None, "particles": None}
    #good_classes_dict = {"particles": None}
    #bad_classes_dict = {"particles": None}

    for class_star_file in class_star_files:
        class_number = int(class_star_file.name[5:8])
        class_star_file = Path(class_star_file).absolute()
        class_star = starfile.read(class_star_file)
        class_particles_df = class_star["particles"]
        class_optics_df = class_star["optics"]
        
        if class_number in good_classes:
            if good_classes_dict["optics"] is None:
                good_classes_dict["optics"] = class_optics_df

            if good_classes_dict["particles"] is None:
                good_classes_dict["particles"] = class_particles_df
            else:
                # Concatenate the good classes
                good_classes_dict["particles"] = pd.concat([good_classes_dict["particles"], class_particles_df], axis=0).reset_index(drop=True)
        else:
            if bad_classes_dict["optics"] is None:
                bad_classes_dict["optics"] = class_optics_df

            if bad_classes_dict["particles"] is None:
                bad_classes_dict["particles"] = class_particles_df
            else:
                # Concatenate the bad classes
                bad_classes_dict["particles"] = pd.concat([bad_classes_dict["particles"], class_particles_df], axis=0).reset_index(drop=True)
        
    good_classes_star_file = Path(classif_directory / "good_classes.star").absolute()
    bad_classes_star_file = Path(classif_directory / "bad_classes.star").absolute()

    print(f"Writing {good_classes_star_file.parent.name}/{good_classes_star_file.name}")
    starfile.write(good_classes_dict, good_classes_star_file, overwrite=overwrite)

    print(f"Writing {bad_classes_star_file.parent.name}/{bad_classes_star_file.name}")
    starfile.write(bad_classes_dict, bad_classes_star_file, overwrite=overwrite)

    return good_classes_dict
