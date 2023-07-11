import subprocess
import time
from pathlib import Path
from ..utils import *


def ctfplotter(
    batch_directory: Path,
    axis_angle: float,
    pixel_size: float,
) -> None:
    # Look for the "frames" and "mdoc" directories
    batch_directory = Path(batch_directory).absolute()
    frames_directory = batch_directory / "frames"
    mdoc_directory = batch_directory / "mdoc"
    if frames_directory.is_dir() and mdoc_directory.is_dir():
        print(
            f"Found 'frames' and 'mdoc' directories: processing all tilt series within {batch_directory}..."
        )
        dirs_to_process = [dir for dir in batch_directory.glob("ts*")]
    # Look for a .mrc in batch_directory
    elif Path(batch_directory / f"{batch_directory}.mrc").is_file():
        dirs_to_process = batch_directory
    # If couldn't find either, exit script
    else:
        print(
            f"Error: Neither found 'frames' and 'mdoc' directories nor a stack to process in {batch_directory}."
        )
        raise SystemExit(0)
    number_to_process = len(dirs_to_process)
    print(f"Found {number_to_process} tilt series to process.")
    print("----")
    init_time = time.time()
    number_processed = 0
    for directory in sorted(dirs_to_process):
        with cd(directory):
            if directory / "sta_ctfplotter.success" in check_job_success(directory):
                print(
                    f'The file "sta_ctfplotter.success" was found. Skipping {directory.name}.'
                )
                number_processed += 1
                continue

            start_time = time.time()
            print(f"Processing {directory.name}.")
            input_stack = directory.name + ".mrc"
            command = [
                "ctfplotter",
                "-InputStack",
                f"{input_stack}",
                "-AxisAngle",
                f"{axis_angle}",
                "-AngleFile",
                f"{input_stack.split('.')[0]}_fid.tlt",
                "-DefocusFile",
                f"{input_stack.split('.')[0]}.defocus",
                "-PixelSize",
                f"{pixel_size / 10.0}",
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
            with open(f"sta_ctfplotter.out", "a") as out, open(
                f"sta_ctfplotter.err",
                "a",
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
    print(f"Writing all defocus values to a f{batch_directory.name}.defocus")
    get_defoci(batch_directory)
    print("Done.")