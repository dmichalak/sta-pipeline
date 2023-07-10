
from pathlib import Path

import subprocess

from ..utils import *


def isonet_predict(
    project_name: str,
    isonet_star_file: Path,
    refine_directory: Path,
    density_percentage: int,
    std_percentage: int,
    gpu_ids: str,
    tomogram_idx_list: str,
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