from pathlib import Path

import subprocess
from typer import Option
from os import PathLike

from ..utils import *
from .._cli import cli, OPTION_PROMPT_KWARGS as PKWARGS


@cli.command(name="isonet_extract", no_args_is_help=True)
def isonet_extract(
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
    isonet_star_file: PathLike = Option(
        default=...,
        help="The path to the star file.",
        **PKWARGS,
    ),
    density_percentage: int = Option(
        default=50,
        help="The density percentage.",
        **PKWARGS,
    ),
    std_percentage: int = Option(
        default=50,
        help="The standard deviation percentage.",
        **PKWARGS,
    ),
    tomogram_idx_list: str = Option(
        default="0,1,2,3,4",
        help="The list of tomogram indices to use.",
        **PKWARGS,
    ),
):
    working_directory = Path(working_directory).absolute()
    isonet_star_file = Path(isonet_star_file).absolute()
    subtomo_folder = f"subtomo_dp{density_percentage}sp{std_percentage}_{project_name}"
    subtomo_star_file = f"subtomo_dp{density_percentage}sp{std_percentage}_{project_name}.star"
    cube_size = 64
    crop_size = 64 + 16

    command = [
        "isonet.py",
        "extract",
        f"{isonet_star_file}",
        "--subtomo_folder",
        f"{subtomo_folder}",
	    "--subtomo_star",
        f"{subtomo_star_file}",
        "--cube_size",
        f"{cube_size}",
        "--crop_size",
        f"{crop_size}",
        "--tomo_idx",
        f"{tomogram_idx_list}",
    ]

    log_out = working_directory / "sta_isonet_extract.out"
    log_err = working_directory / "sta_isonet_extract.err"
    with open(log_out, "a") as out, open(log_err, "a") as err:
        result = subprocess.run(command, stdout=out, stderr=err)