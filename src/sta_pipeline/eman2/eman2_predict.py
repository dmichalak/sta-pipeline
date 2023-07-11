import subprocess
from pathlib import Path
from ..utils import *


def eman2_predict(
    eman2_directory: Path,
    batch_directory: Path,
) -> None:
    """Predict the locations of particles in tomograms using a trained network."""
    eman2_directory = Path(eman2_directory).absolute()
    batch_directory = Path(batch_directory).absolute()

    tomogram_path_list = get_tomogram_paths(batch_directory)
    tomogram_paths = ",".join(tomogram_path_list)

    trained_network = eman2_directory / "trained_network.hdf"

    command = [
        "e2tomoseg_convnet.py",
        "--nnet=" + str(trained_network),
        "--tomograms=" + str(tomogram_paths),
        "--applying",
        "--threads=32",
        "--device=gpu",
    ]


    log_out = eman2_directory / "sta_isonet_deconv.out"
    log_err = eman2_directory/ "sta_isonet_deconv.err"
    with open(log_out, "a") as out, open(log_err, "a") as err:
        result = subprocess.run(command, stdout=out, stderr=err)