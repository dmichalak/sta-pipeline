from pathlib import Path

import pandas as pd
from typer import Option
from os import PathLike
import starfile

from .get_defoci import get_defoci
from ..utils import *
from .._cli import cli, OPTION_PROMPT_KWARGS as PKWARGS


@cli.command(name="isonet_setup", no_args_is_help=True)
def isonet_setup(
    data_directory: PathLike = Option(
        default=...,
        help="The path to the directory containing all ts directories.",
        **PKWARGS,
    ),
    working_directory: PathLike = Option(
        default=...,
        help="The directory to output all isonet files.",
        **PKWARGS,
    ),
    project_name: str = Option(
        default="isonet",
        help="The name of the project.",
        **PKWARGS,
    ),
    pixel_size: float = Option(
        default=10.825,
        help="The pixel size in angstrom.",
        **PKWARGS,
    ),
) -> None:
    """
    Create the star file for isonet.

    Parameters
    ----------
    data_directory : PathLike
        The path to the directory containing all ts directories.
    working_directory : PathLike
        The directory to output all isonet files.
    project_name : str
        The name of the project.
    pixel_size : float
        The pixel size in angstrom.

    Returns
    -------
    isonet_star_file : PathLike
        The path to the star file.
    """

    data_directory = Path(data_directory).absolute()
    working_directory = Path(working_directory).absolute()

    # get the defocus values from the ctfplotter output files
    ts_defoci_dict = get_defoci(data_directory)

    # create the a DataFrame for the star file
    isonet_star_df = pd.DataFrame()
    isonet_star_df["rlnIndex"] = range(1,len(ts_defoci_dict)+1)
    isonet_star_df["rlnMicrographName"] = [f"{data_directory}/{ts_name}/{ts_name}_rec.mrc" for ts_name in ts_defoci_dict.keys()]
    isonet_star_df["rlnPixelSize"] = pixel_size
    isonet_star_df["rlnDefocus"] = ts_defoci_dict.values()
    isonet_star_df["rlnNumberSubtomo"] = 60

    # write the star file
    isonet_star_filepath = working_directory / f"{project_name}.star"
    starfile.write(isonet_star_df, isonet_star_filepath, overwrite=True)