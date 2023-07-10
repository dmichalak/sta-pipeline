
from pathlib import Path

import subprocess
from typer import Option
from os import PathLike

from ..utils import *
from .._cli import cli, OPTION_PROMPT_KWARGS as PKWARGS


@cli.command(name="isonet_refine", no_args_is_help=True)
def isonet_refine(
    working_directory: PathLike = Option(
        default=...,
        help="The directory to output all isonet files.",
        **PKWARGS,
    ),
    scratch_directory: PathLike = Option(
        default=...,
        help="The temporary directory used for training.",
        **PKWARGS,
    ),
    subtomo_star_file: PathLike = Option(
        default=...,
        help="The path to the star file.",
        **PKWARGS,
    ),
    project_name: str = Option(
        default="isonet",
        help="The name of the project.",
        **PKWARGS,
    ),
    gpu_ids: str = Option(
        default="0",
        help="The GPU IDs to use.",
        **PKWARGS,
    ),
    n_cpu: int = Option(
        default=4,
        help="The number of CPUs to use.",
        **PKWARGS,
    ),
    iterations: int = Option(
        default=30,
        help="The number of iterations to train for.",
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
):
    working_directory = Path(working_directory).absolute()
    scratch_directory = Path(scratch_directory).absolute()
    subtomo_star_file = Path(subtomo_star_file).absolute()
    result_directory = working_directory / f"refine_dp{density_percentage}sp{std_percentage}_{project_name}"

    log_level = ""
    noise_level = "0.05,0.1,0.15,0.2"
    noise_start_iter = "11,16,21,26"
    learning_rate = "0.0004"
    drop_out = "0.3"
    kernel = "(3,3,3)"
    unet_depth = "3"

    command = [
        "isonet.py",
        "refine",
        f"{subtomo_star_file}",
        "--gpuID",
        f"{gpu_ids}",
        "--preprocessing_ncpus",
        f"{n_cpu}",
        "--iterations",
        f"{iterations}",
        "--result_dir",
        f"{result_directory}",
        "--log_level",
        f"{log_level}",
        "--data_dir",
        f"{scratch_directory}",
        "--noise_level",
        f"{noise_level}",
        "--noise_start_iter",
        f"{noise_start_iter}",
        "--learning_rate",
        f"{learning_rate}",
        "--drop_out",
        f"{drop_out}",
        "--kernel",
        f"{kernel}",
        "--unet_depth",
        f"{unet_depth}",
    ]

    log_out = working_directory / "sta_isonet_refine.out"
    log_err = working_directory / "sta_isonet_refine.err"
    with open(log_out, "a") as out, open(log_err, "a") as err:
        result = subprocess.run(command, stdout=out, stderr=err)