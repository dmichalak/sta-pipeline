from pathlib import Path

import subprocess
from typer import Option
from os import PathLike

from ..utils import *
from .._cli import cli, OPTION_PROMPT_KWARGS as PKWARGS

@cli.command(name="isonet_deconv", no_args_is_help=True)
def isonet_deconv(
    working_directory: PathLike = Option(
        default=...,
        help="The directory to output all isonet files.",
        **PKWARGS,
    ),
    isonet_star_file: PathLike = Option(
        default=...,
        help="The path to the star file.",
        **PKWARGS,
    ),
    project_name: str = Option(
        default="isonet",
        help="The name of the project.",
        **PKWARGS,
    ),
    voltage: int = Option(
        default=300,
        help="The voltage of the microscope.",
        **PKWARGS,
    ),
    cs: float = Option(
        default=2.7,
        help="The spherical aberration of the microscope in mm.",
        **PKWARGS,
    ),
    snr_falloff: float = Option(
        default=0.7,
        help="The signal to noise ratio falloff.",
        **PKWARGS,
    ),
    deconv_strength: float = Option(
        default=1.0,
        help="The deconvolution strength.",
        **PKWARGS,
    ),
    n_cpu: int = Option(
        default=4,
        help="The number of CPUs to use.",
        **PKWARGS,
    ),
    tomogram_idx_list: str = Option(
        default="0,1,2,3,4",
        help="The list of tomogram indices to use.",
        **PKWARGS,
    ),
 ) -> None:
    """
    Deconvolve the tilt series using isonet.
    
    Parameters
    ----------
    working_directory : PathLike
        The directory to output all isonet files.
    isonet_star_file : PathLike
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