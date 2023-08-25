from pathlib import Path
from typing import Optional

import starfile

def rln_split_classif_star(
        classif_star_file: Path,
        overwrite: Optional[bool] = False,
) -> dict:
    """ Split up the run_it025_data.star file into separate star files for each class specified by rlnClassNumber.

        Args:
                classif_star_file (Path): Path to the run_it025_data.star file
                overwrite (bool): Whether to overwrite existing star files

        Returns:
                classes_dict (dict): Dictionary of "particles" and "optics" for each class

    """

    classif_star_file = Path(classif_star_file).absolute()
    classif_star = starfile.read(classif_star_file)
    classif_particles_df = classif_star["particles"]
    classif_optics_df = classif_star["optics"]

    # Create a dictionary of classes
    classes_dict = {}

    # Get the list of class numbers from rlnClassNumber
    class_number_list = sorted(classif_particles_df["rlnClassNumber"].unique())

    for class_number in class_number_list:

        class_star_file = Path(classif_star_file.parent / f"class_{class_number}_it025_data.star").absolute()
        classes_dict[class_number] = {"optics": classif_optics_df}
        classes_dict[class_number]["particles"] = classif_particles_df[classif_particles_df["rlnClassNumber"] == class_number]

        # Write the star file
        print(f"Writing {class_star_file.parent.name}/{class_star_file.name}")
        starfile.write(classes_dict[class_number], class_star_file, overwrite=overwrite)
    
    return classes_dict

