from pathlib import Path

import subprocess

from ..utilities.utils import *


def isonet_refine(
    working_directory: Path,
    scratch_directory: Path,
    subtomo_star_file: Path,
    project_name: str,
    gpu_ids: str,
    n_cpu: int,
    iterations: int,
    density_percentage: int,
    std_percentage: int,
) -> Path:
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

    return result_directory