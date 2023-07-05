import click
import subprocess
import time
from pathlib import Path
from ..utils import *


def sta_ctfplotter(
    input_directory: Path,
    axis_angle: float,
    pixel_size: float,
) -> None:
    # Look for the "frames" and "mdoc" directories
    input_directory = Path(input_directory).absolute()
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
    number_to_process = len(dirs_to_process)
    print(f"Found {number_to_process} tilt series to process.")
    init_time = time.time()
    number_processed = 0
    for directory in dirs_to_process:
        with cd(directory):
            if "sta_ctfplotter.success" in check_job_success(directory):
                print(
                    f'The file "sta_ctfplotter.success" was found. Skipping {directory.name}.'
                )
                number_processed+=1
                continue

            start_time = time.time()
            print(f"Processing {directory.name}.")
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
            with open(f"sta_ctfplotter_{directory.name}.out", "a") as out, open(
                f"sta_ctfplotter_{directory.name}.err", "a",
            ) as err:
                result = subprocess.run(command, stdout=out, stderr=err)
            job_success(directory, "sta_ctfplotter")
            number_processed += 1
            end_time = time.time()  # Stop measuring the time for this iteration
            processing_time = end_time - start_time
            minutes, seconds = divmod(processing_time, 60)
            print(f"{directory.name} took {int(minutes)} min {int(seconds)} sec.")
            # Report how long the job has been running
            current_time = time.time() - init_time 
            minutes, seconds = divmod(current_time, 60)
            print(f"{number_processed} of {number_to_process} completed.")
            print(f"Total time elapsed: {int(minutes)} min {int(seconds)} sec")
            # Report how long the job is expected to run
            expected_time = number_to_process / (number_processed / current_time)
            minutes, seconds = divmod(expected_time, 60)
            print(f"Total time expected: {int(minutes)} min {int(seconds)} sec")
            print("----")



@click.command()
@click.option(
    "--input_directory",
    "-i",
    required=True,
    help="Input directory containing either an MRC tilt series or, for batch processing, 'frames', 'mdoc', and tilt series directories.",
)
@click.option(
    "--axis_angle",
    "-aa",
    default=178.9,
    show_default=True,
    help="Tilt axis angle in degrees.",
)
@click.option(
    "--pixel_size",
    "-ps",
    default=1.0825,
    show_default=True,
    help="Pixel size in ångströms.",
)
def cli(input_directory, axis_angle, pixel_size):
    sta_ctfplotter(input_directory, axis_angle, pixel_size)
