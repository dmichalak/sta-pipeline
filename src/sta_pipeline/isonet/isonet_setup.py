from pathlib import Path

import pandas as pd
import starfile

from ..utilities.utils import *


def isonet_setup(
    data_directory: Path,
    working_directory: Path,
    project_name: str,
    pixel_size: float,
) -> Path:
    """
    Create the star file for isonet.

    Parameters
    ----------
    data_directory : Path
        The path to the directory containing all ts directories.
    working_directory : Path
        The directory to output all isonet files.
    project_name : str
        The name of the project.
    pixel_size : float
        The pixel size in angstrom.

    Returns
    -------
    isonet_star_file : Path
        The path to the star file.
    """

    data_directory = Path(data_directory).absolute()
    working_directory = Path(working_directory).absolute()

    # get the defocus values from the ctfplotter output files
    ts_defoci_dict = get_defoci(data_directory)

    # create the a DataFrame for the star file
    isonet_star_df = pd.DataFrame()
    isonet_star_df["rlnIndex"] = range(1,len(ts_defoci_dict)+1)
    isonet_star_df["rlnMicrographName"] = [f"{data_directory}/{ts_name}/{ts_name}_b10_rec.mrc" for ts_name in ts_defoci_dict.keys()]
    isonet_star_df["rlnPixelSize"] = pixel_size
    isonet_star_df["rlnDefocus"] = ts_defoci_dict.values()
    isonet_star_df["rlnNumberSubtomo"] = 60

    # write the star file
    isonet_star_filepath = working_directory / f"{project_name}.star"
    starfile.write(isonet_star_df, isonet_star_filepath, overwrite=True)
    
    return isonet_star_filepath