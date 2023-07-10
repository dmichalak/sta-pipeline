import subprocess
import click
import time
from pathlib import Path
from typing import Optional
from multiprocessing import Pool
from ..utils import *

def alignframes(
    stack_data
    #input_directory,mdoc_file,align_binning,sum_binning,ts_number,
) -> None:

    input_directory = stack_data[0]
    mdoc_file = stack_data[1]
    align_binning = stack_data[2]
    sum_binning = stack_data[3]
    ts_number = stack_data[4]
    frames_directory = input_directory / "frames"

    if mdoc_file.stat().st_size < 10 * 1024:
    # if the mdoc file is bigger than 10 kB, to make sure it corresponds to a full tilt series
        print(
            "This mdoc doesn't seem to correspond to a tilt series. Skipping it..."
        )
        return
    ts_directory = input_directory / Path(f"ts{ts_number:03}").absolute()
    output_image_file = ts_directory / Path(f"ts{ts_number:03}.mrc")

    if not ts_directory.exists():
        Path.mkdir(ts_directory)

    # Check if this tilt stack has already been processed
    if ts_directory / "sta_alignframes.success" in check_job_success(ts_directory):
        print(
            f'The file "sta_alignframes.success" was found. Skipping {ts_directory.name}.'
        )
        ts_number += 1
        return
    print(f"Processing {ts_directory.name}.")
    start_time = time.time()  # Start measuring the time for this iteration
    command = [
        "alignframes",
        "-MetadataFile",
        mdoc_file,
        "-PathToFramesInMdoc",
        frames_directory,
        "-OutputImageFile",
        output_image_file,
        "-binning",
        str(align_binning) + " " + str(sum_binning),
        "-ModeToOutput",
        "2",
    ]

    with open(f"{ts_directory.name}/sta_alignframes.out", "a") as out, open(
        f"{ts_directory.name}/sta_alignframes.err", "a",
    ) as err:
        result = subprocess.run(command, stdout=out, stderr=err)

    # output_image_file.replace(output_image_file.with_suffix(f"_bin{align_binning}.st"))
    if int(align_binning) * int(sum_binning) > 1:
        output_image_file.rename(
            ts_directory / (output_image_file.stem + f"_bin{int(sum_binning)}.mrc")
        )

    command = ["cp", mdoc_file.as_posix(), ts_directory.as_posix()]
    result = subprocess.run(command)
    ts_number += 1
    job_success(ts_directory, "sta_alignframes")
    end_time = time.time()  # Stop measuring the time for this iteration
    processing_time = end_time - start_time
    minutes, seconds = divmod(processing_time, 60)
    print(f"{ts_directory.name} took {int(minutes)} min {int(seconds)} sec.")

def sta_alignframes_multiprocessing(
    input_directory: Path,
    align_binning: int,
    sum_binning: int,
    num_processes: int,
) -> None:
    input_directory = Path(input_directory).absolute()
    # Look for the "frames" and "mdoc" directories
    frames_directory = input_directory / "frames"
    mdoc_directory = input_directory / "mdoc"
    if frames_directory.is_dir() and mdoc_directory.is_dir():
        print(
            f"Found 'frames' and 'mdoc' directories: processing all tilt series within {mdoc_directory}..."
        )
    # If couldn't find, exit script
    else:
        print(
            f"Error: Did not find 'frames' and 'mdoc' directories in {input_directory.name}."
        )
        raise SystemExit(0)


    stacks_to_process = []
    ts_number = 1

    for mdoc_file in sorted(mdoc_directory.glob("*.mrc.mdoc")):
        stacks_to_process.append([input_directory, mdoc_file, align_binning, sum_binning, ts_number])
        ts_number+=1

    with Pool(processes=int(num_processes)) as pool:
        pool.map(alignframes, stacks_to_process)




@click.command()
@click.option(
    "--input_directory",
    "-i",
    required=True,
    help="Input directory containing 'frames' and 'mdoc' directories.",
)
@click.option(
    "--align_binning",
    "-ab",
    default=5,
    help="Binning to be used for movie frame alignment.",
)
@click.option(
    "--sum_binning",
    "-sb",
    default=5,
    help="Binning to be used for movie frame summing. This will be the binning of the tilt series. Make sure to set the binning for the tomogram reconstruction accordingly. (e.g., setting bin=2 for reconstruction using a stack generated at --sum_binning=5 will result in a final binning of 10.",
)
@click.option(
    "--num_processes",
    "-n",
    required=True,
    help="Number of parallel processes."
)
def cli(input_directory, align_binning, sum_binning, num_processes):
    sta_alignframes_multiprocessing(input_directory, align_binning, sum_binning, num_processes)
