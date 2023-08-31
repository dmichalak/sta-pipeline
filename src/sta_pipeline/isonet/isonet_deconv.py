from pathlib import Path

import subprocess

from ..utilities.utils import *

def isonet_deconv(
    working_directory: Path,
    isonet_star_file: Path,
    project_name: str,
    voltage: int,
    cs: float,
    snr_falloff: float,
    deconv_strength: float,
    n_cpu: int,
    tomogram_idx_list: str,
 ) -> None:
    """
    Deconvolve the tilt series using isonet.
    
    Parameters
    ----------
    working_directory : Path
        The directory to output all isonet files.
    isonet_star_file : Path
        The path to the star file.
    project_name : str
        The name of the project.
    voltage : int
        The voltage of the microscope.
    cs : float
        The spherical aberration of the microscope.
    snr_falloff : float
        The signal to noise ratio falloff.
    deconv_strength : float
        The deconvolution strength.
    n_cpu : int
        The number of CPUs to use.
    tomogram_idx_list : list
        The list of tomogram indices to use.

    Returns
    -------
    None
    """
    
    working_directory = Path(working_directory).absolute()
    isonet_star_file = Path(isonet_star_file).absolute()

    highpass_nyquist = 0.02

    deconv_folder = working_directory / f"deconv_snr{snr_falloff}_{project_name}"
    deconv_folder.mkdir(exist_ok=True)
    if tomogram_idx_list == "all":
        command = [
            "isonet.py",
            "deconv",
            f"{isonet_star_file}",
            "--deconv_folder",
            f"{deconv_folder}",
            "--voltage",
            f"{voltage}",
            "--cs",
            f"{cs}",
            "--snrfalloff",
            f"{snr_falloff}",
            "--deconvstrength",
            f"{deconv_strength}",
            "--highpassnyquist",
            f"{highpass_nyquist}",
            "--ncpu",
            f"{n_cpu}",
        ]
    else:
        command = [
            "isonet.py",
            "deconv",
            f"{isonet_star_file}",
            "--deconv_folder",
            f"{deconv_folder}",
            "--voltage",
            f"{voltage}",
            "--cs",
            f"{cs}",
            "--snrfalloff",
            f"{snr_falloff}",
            "--deconvstrength",
            f"{deconv_strength}",
            "--highpassnyquist",
            f"{highpass_nyquist}",
            "--ncpu",
            f"{n_cpu}",
            "--tomo_idx",
            f"{tomogram_idx_list}",
        ]
    log_out = working_directory / "sta_isonet_deconv.out"
    log_err = working_directory / "sta_isonet_deconv.err"
    with open(log_out, "a") as out, open(log_err, "a") as err:
        result = subprocess.run(command, stdout=out, stderr=err)