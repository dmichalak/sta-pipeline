from pathlib import Path
from typing import Optional
import subprocess
import pandas as pd
from ..utilities.utils import *

def eman2_training(
    eman2_trainset: Path,
    learning_rate: float,
    iterations: int,
    continue_from: Optional[Path] = None,
    gpu_id: Optional[int] = 0,
) -> None:

    eman2_trainset = Path(eman2_trainset).absolute()
    eman2_directory = eman2_trainset.parent

    if continue_from is None or continue_from == "None":
        command = [
            "e2tomoseg_convnet.py",
            f"--trainset={eman2_trainset}",
            f"--learnrate={learning_rate}",
            f"--niter={iterations}",
            "--ncopy=1",
            "--batch=20",
            "--nkernel=40,40,1",
            "--ksize=15,15,15",
            "--poolsz=2,1,1",
            "--trainout",
            "--training",
            f"--device=gpu{gpu_id}",
        ]
        with open(eman2_directory / f"training_{eman2_trainset.stem}.out", "a") as out, open(
            eman2_directory / f"training_{eman2_trainset.stem}.err", "a"
        ) as err:
            result = subprocess.run(command, stdout=out, stderr=err)
    else:
        command = [
            "e2tomoseg_convnet.py",
            f"--trainset={eman2_trainset}",
            f"--from_trained={continue_from}",
            f"--learnrate={learning_rate}",
            f"--niter={iterations}",
            "--ncopy=1",
            "--batch=20",
            "--nkernel=40,40,1",
            "--ksize=15,15,15",
            "--poolsz=2,1,1",
            "--trainout",
            "--training",
            "--device=gpu",
        ]
        with open(eman2_directory / f"training_{eman2_trainset.stem}.out", "a") as output:
            output.write("--------------------\n")
            output.write(f"Learning rate: {learning_rate}\n")
            output.write(f"Iterations: {iterations}\n")
            output.write("--------------------\n")
        with open(eman2_directory / f"training_{eman2_trainset.stem}.out", "a") as out, open(
            eman2_directory / f"training_{eman2_trainset.stem}.err", "a"
        ) as err:
            result = subprocess.run(command, stdout=out, stderr=err)
    with open(eman2_directory / f"training_{eman2_trainset.stem}.out", "r") as input:
        lines = input.readlines()
    with open(eman2_directory / f"training_{eman2_trainset.stem}.out", "w") as output:
        for line in lines:
            if "=" not in line and len(line) > 5:
                output.write(line.strip("\n") + "\n")
    with open(eman2_directory / f"training_{eman2_trainset.stem}.out", "r") as input:
        lines = input.readlines()
        for line in lines:
            print(line.strip("\n"))
