from pathlib import Path

import subprocess

from ..utils import *


def isonet_extract(
    working_directory: Path,
    project_name: str,
    isonet_star_file: Path,
    density_percentage: int,
    std_percentage: int,
    tomogram_idx_list: str,
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