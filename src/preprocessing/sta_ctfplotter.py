import click
import subprocess
from pathlib import Path
from ..utils import *


def sta_ctfplotter(
    input_directory: Path,
    axis_angle: float,
    pixel_size: float,
) -> None:
    # Look for the "frames" and "mdoc" directories
    frames_directory = input_directory / "frames"
    mdoc_directory = input_directory / "mdoc"
    if frames_directory.is_dir() and mdoc_directory.is_dir():
        print(
            f"Found 'frames' and 'mdoc' directories: processing all tilt series within {input_directory}..."
        )
        dirs_to_process = [dir for dir in input_directory.glob("ts*")]
    # Look for a .mrc in input_directory
    elif Path(input_directory / f"{input_directory}.mrc").is_file():
        dirs_to_process = input_directory
    # If couldn't find either, exit script
    else:
        print(
            f"Error: Neither found 'frames' and 'mdoc' directories nor a stack to process in {input_directory}."
        )
        raise SystemExit(0)

    for directory in dirs_to_process:
        with cd(directory):
            input_stack = directory.name + ".mrc"
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
    "--input_directory",
    "-i",
    required=True,
    help="Input directory containing either an MRC tilt series or, for batch processing, 'frames', 'mdoc', and aligned tilt series directories.",
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
    help="Pixel size in ångströms.",
)
def cli(input_directory, axis_angle, pixel_size):
    sta_ctfplotter(input_directory, axis_angle, pixel_size)
