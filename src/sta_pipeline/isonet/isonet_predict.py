
from pathlib import Path

import time
import subprocess
from typer import Option
from os import PathLike

from ..utils import *
from .._cli import cli, OPTION_PROMPT_KWARGS as PKWARGS


@cli.command(name="isonet_predict", no_args_is_help=True)
def isonet_predict(
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
    refine_directory: PathLike = Option(
        default=...,
        help="The path to the refine directory.",
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
    gpu_ids: str = Option(
        default="0",
        help="The GPU IDs to use.",
        **PKWARGS,
    ),
    tomogram_idx_list: str = Option(
        default="0,1,2,3,4",
        help="The list of tomogram indices to use.",
        **PKWARGS,
    ),
):
    isonet_star_file = Path(isonet_star_file).absolute()
    refine_directory = Path(refine_directory).absolute()
    trained_model = refine_directory / "model_iter30.h5"
    output_directory = refine_directory / ".." / f"predict_dp{density_percentage}sp{std_percentage}_{project_name}"
    cube_size = 64
    crop_size = 64 + 16

    command = [
        "isonet.py",
        'predict',
        f"{isonet_star_file}",
        f"{trained_model}",
        '--output_dir',
        f"{output_directory}",
        '--gpuID',
        f"{gpu_ids}",
        '--cube_size',
        f"{cube_size}",
        '--crop_size',
        f"{crop_size}",
        '--tomo_idx',
        f"{tomogram_idx_list}",
    ]

    log_out = refine_directory / ".." / "sta_isonet_predict.out"
    log_err = refine_directory / ".." / "sta_isonet_predict.err"
    with open(log_out, "a") as out, open(log_err, "a") as err:
        result = subprocess.run(command, stdout=out, stderr=err)