import click
import subprocess
from pathlib import Path
from ..utils import *


def sta_ctfplotter(
    batch_directory: Path,
    stack_directory: Path,
    axis_angle: float,
    pixel_size: float,
) -> None:
    if batch_directory is None:
        stack_directory = Path(stack_directory).absolute()
        dirs_to_process = [stack_directory]
    else:
        batch_directory = Path(batch_directory).absolute()
        dirs_to_process = [dir for dir in batch_directory.glob("ts*")]
    for directory in dirs_to_process:
        with cd(directory):
            input_stack = (
                directory.parent.name + "_" + directory.name + ".mrc"
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
            with open(f"sta_ctfplotter_{directory.name}.out", "w") as out, open(
                f"sta_ctfplotter_{directory.name}.err", "w"
            ) as err:
                result = subprocess.run(command, stdout=out, stderr=err)


@click.command()
@click.option(
    "--batch_directory",
    "-b",
    help="Path to the batch directory.",
)
@click.option(
    "--stack_directory",
    "-s",
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
def cli(batch_directory, stack_directory, axis_angle, pixel_size):
    sta_ctfplotter(batch_directory, stack_directory, axis_angle, pixel_size)
