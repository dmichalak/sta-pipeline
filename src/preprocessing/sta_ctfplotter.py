import click
import subprocess
from pathlib import Path
from ..utils import *


def sta_ctfplotter(
    batch_dir: Path, 
    stack_dir: Path, 
    stack_extension: str, 
    axis_angle: float, 
    pixel_size: float,
    ) -> None:

    if batch_dir is None:
        stack_dir = Path(stack_dir).absolute()
        dirs_to_process = [stack_dir]
    else:
        batch_dir = Path(batch_dir).absolute()
        dirs_to_process = [dir for dir in batch_dir.glob("ts*")]
    for directory in dirs_to_process:
        with cd(directory):
            input_stack = (
                directory.parent.name + "_" + directory.name + "." + stack_extension
            )
            command = [
                "ctfplotter",
                "-InputStack",
                input_stack,
                "-AxisAngle",
                str(axis_angle),
                "-AngleFile",
                input_stack.split(".")[0] + "_fid.tlt",
                "-DefocusFile",
                input_stack.split(".")[0] + ".defocus",
                "-PixelSize",
                str(pixel_size / 10),
                "-CropToPixelSize",
                "0.4",
                "-Voltage",
                "300",
                "-SphericalAberration",
                "2.7",
                "-ExpectedDefocus",
                "6000",
                "-AutoFitRangeAndStep",
                "0,1",
                "-UseExpectedDefForAuto",
                "-VaryExponentInFit",
                "-SearchAstigmatism",
                "-SaveAndExit",
            ]
            with open(f"sta_ctfplotter_{directory.name}.out", "w") as out, open(f"sta_ctfplotter_{directory.name}.err", "w") as err:
                result = subprocess.run(command, stdout=out, stderr=err)


@click.command()
@click.option(
    "--batch_dir",
    "-b",
    help="Path to the batch directory.",
)
@click.option(
    "--stack_dir",
    "-s",
    help="Help text",
)
@click.option(
    "--stack_extension",
    "-ext",
    default=".mrc",
    help="Help text",
)
@click.option(
    "--axis_angle",
    "-aa",
    default=178.9,
    help="Help text",
)
@click.option(
    "--pixel_size",
    "-ps",
    default=1.0825,
    help="Help text",
)
def cli(batch_dir, stack_dir, stack_extension, axis_angle, pixel_size):
    sta_ctfplotter(batch_dir, stack_dir, stack_extension, axis_angle, pixel_size)
