import subprocess
from typing import Optional
from pathlib import Path
import pandas as pd

from ..utilities.utils import *


def eman2_predict(
    trained_network: Path,
    corrected_tomograms: Path,
    gpu_id: Optional[int] = 0,
) -> None:
    """Predict the locations of particles in tomograms using a trained network."""

    trained_network = Path(trained_network).absolute()
    corrected_tomograms = Path(corrected_tomograms).absolute()
    eman2_directory = corrected_tomograms.parent

    tomogram_path_list = [
        f"{tomogram}" for tomogram in sorted(corrected_tomograms.glob("*.hdf"))
    ]
    tomogram_paths = ",".join(tomogram_path_list)

    command = [
        "e2tomoseg_convnet.py",
        f"--nnet={trained_network}",
        f"--tomograms={tomogram_paths}",
        "--applying",
        "--threads=32",
        f"--device=gpu{gpu_id}",
    ]

    log_out = eman2_directory / "sta_eman2_predict.out"
    log_err = eman2_directory / "sta_eman2_predict.err"
    with open(log_out, "a") as out, open(log_err, "a") as err:
        result = subprocess.run(command, stdout=out, stderr=err)
