import subprocess
import time
from pathlib import Path
from multiprocessing import Pool
from ..utilities.utils import *
from .write_mdoc_to_ts_list import write_mdoc_to_ts_list

def alignframes(
    stack_data
) -> None:

    batch_directory = stack_data[0]
    mdoc_file = stack_data[1]
    align_binning = stack_data[2]
    sum_binning = stack_data[3]
    ts_number = stack_data[4]
    frames_directory = batch_directory / "frames"

    if mdoc_file.stat().st_size < 10 * 1024:
    # if the mdoc file is bigger than 10 kB, to make sure it corresponds to a full tilt series
        print(
            f"The mdoc {mdoc_file} is smaller than expected. Skipping it..."
        )
        return
    ts_directory = batch_directory / Path(f"ts_{ts_number:03}").absolute()
    output_image_file = ts_directory / Path(f"ts_{ts_number:03}.mrc")

    if not ts_directory.exists():
        Path.mkdir(ts_directory)

    # Check if this tilt stack has already been processed
    if ts_directory / "sta_alignframes.success" in check_job_success(ts_directory):
        print(
            f'The file "sta_alignframes.success" was found. Skipping {ts_directory.name}.'
        )
        ts_number += 1
        return
    
    # Copy the mdoc file to the ts directory
    command = ["cp", mdoc_file.as_posix(), ts_directory.as_posix()]
    result = subprocess.run(command)


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
        with cd(ts_directory):
            result = subprocess.run(command, stdout=out, stderr=err)

    # output_image_file.replace(output_image_file.with_suffix(f"_bin{align_binning}.st"))
    if int(sum_binning) > 1:
        output_image_file.rename(
            ts_directory / (output_image_file.stem + f"_bin{int(sum_binning)}.mrc")
        )

    ts_number += 1
    job_success(ts_directory, "sta_alignframes")
    end_time = time.time()  # Stop measuring the time for this iteration
    processing_time = end_time - start_time
    minutes, seconds = divmod(processing_time, 60)
    print(f"{ts_directory.name} took {int(minutes)} min {int(seconds)} sec.")

    # Write/append mdoc file name and ts_*** to a text file in the batch_directory
    with open(batch_directory / "mdoc_to_ts.txt", "a") as ts_list:
        ts_list.write(f"{mdoc_file.name} {ts_directory.name}\n")


def alignframes_mp(
    batch_directory: Path,
    align_binning: int,
    sum_binning: int,
    num_processes: int,
) -> None:
    batch_directory = Path(batch_directory).absolute()
    # Look for the "frames" and "mdoc" directories
    frames_directory = batch_directory / "frames"
    mdoc_directory = batch_directory / "mdoc"
    if frames_directory.is_dir() and mdoc_directory.is_dir():
        print(
            f"Found 'frames' and 'mdoc' directories: processing all tilt series within {mdoc_directory}..."
        )
    # If couldn't find, exit script
    else:
        print(
            f"Error: Did not find 'frames' and 'mdoc' directories in {batch_directory.name}."
        )
        raise SystemExit(0)


    stacks_to_process = []
    ts_number = 1

    for mdoc_file in sorted(mdoc_directory.glob("*.mrc.mdoc")):
        stacks_to_process.append([batch_directory, mdoc_file, align_binning, sum_binning, ts_number])
        ts_number+=1

    with Pool(processes=int(num_processes)) as pool:
        pool.map(alignframes, stacks_to_process)

    write_mdoc_to_ts_list(batch_directory, overwrite=False)