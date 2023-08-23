from pathlib import Path

import subprocess

from ..utilities.utils import *

def isonet_mask(
    working_directory: Path,
    isonet_star_file: Path,
    project_name: str,
    density_percentage: int,
    std_percentage: int,
    z_crop: float,
    tomogram_idx_list: str,
 ) -> None:
    """
    Create the mask for isonet.

    Parameters
    ----------
    working_directory : Path
        The directory to output all isonet files.
    isonet_star_file : Path
        The path to the star file.
    project_name : str
        The name of the project.
    density_percentage : float
        The density percentage.
    std_percentage : float
        The standard deviation percentage.
    z_crop : float
        The z crop.
    tomogram_idx_list : list
        The list of tomogram indices to use.

    Returns
    -------
    None
    """
    working_directory = Path(working_directory).absolute()
    isonet_star_file = Path(isonet_star_file).absolute()
    mask_folder = working_directory / f"mask_dp{density_percentage}sp{std_percentage}_{project_name}"

    """ 
    patch_size: The size of the box from which the max-filter and std-filter are calculated

    From IsoNet_v).2_Tutorial.md: "Since this demo tomogram has a bin-factor of 4, 
    a smaller Gaussian filter can smooth out noise and keep the fine structure. We set patch_size to 2." 
    patch_size = 2 was for 18.6 A/px, so for 10.825 A/px, we use patch_size = 4
    """
    patch_size = 4

    command = [
    	"isonet.py",
        "make_mask",
        f"{isonet_star_file}",
        "--mask_folder",
        f"{mask_folder}",
 		"--density_percentage",
        f"{density_percentage}",
        "--std_percentage",
        f"{std_percentage}",
 		"--z_crop",
        f"{z_crop}",
        "--patch_size",
        f"{patch_size}",
        "--tomo_idx",
        f"{tomogram_idx_list}",
    ]

    log_out = working_directory / "sta_isonet_mask.out"
    log_err = working_directory / "sta_isonet_mask.err"
    with open(log_out, "a") as out, open(log_err, "a") as err:
        result = subprocess.run(command, stdout=out, stderr=err)