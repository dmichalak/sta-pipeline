import subprocess
import time
from pathlib import Path
from ..utils import *


def batchruntomo(
    batch_directory: Path,
    directive_file: Path,
    n_cpus: int,
    starting_step: float,
    ending_step: float,
    binning: int,
    force: bool,
) -> None:
    # Look for the "frames" and "mdoc" directories
    batch_directory = Path(batch_directory).absolute()
    directive_file = Path(directive_file).absolute()

    frames_directory = batch_directory / "frames"
    mdoc_directory = batch_directory / "mdoc"
    if frames_directory.is_dir() and mdoc_directory.is_dir():
        print(
            f"Found 'frames' and 'mdoc' directories: processing all tilt series within {batch_directory}..."
        )
        dirs_to_process = [dir for dir in batch_directory.glob("ts*")]
    # Look for a .mrc in batch_directory
    elif (
        Path(batch_directory / f"{batch_directory}.mrc").is_file()
        or Path(batch_directory / f"{batch_directory}_bin{binning}.mrc").is_file()
    ):
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
    number_found = 0
    for directory in sorted(dirs_to_process):
        if (
            directory / "sta_batchruntomo.success" in check_job_success(directory)
            and force == False
        ):
            print(
                f'The file "sta_batchruntomo.success" was found. Skipping {directory.name}.'
            )
            number_found += 1
            continue

        rootname_binned = f"{directory.name}_bin{binning}"
        if Path(rootname_binned + ".mrc").is_file():
            rootname = rootname_binned
        else:
            rootname = f"{directory.name}"
        print(f"Processing {rootname}.")
        start_time = time.time()
        command = [
            "batchruntomo",
            "-DirectiveFile",
            f"{directive_file}",
            "-RootName",
            f"{rootname}",
            "-CurrentLocation",
            f"{directory}",
            "-NamingStyle",
            "1",
            "-CPUMachineList",
            f"localhost:{n_cpus}",
            "-GPUMachineList",
            "1",
            "-StartingStep",
            f"{starting_step}",
            "-EndingStep",
            f"{ending_step}",
            "-MakeComExtensionPcm",
            "0",
        ]

        with open(directory / "sta_batchruntomo.out", "a") as out, open(
            directory / "sta_batchruntomo.err",
            "a",
        ) as err:
            result = subprocess.run(command, stdout=out, stderr=err)
        job_success(directory, "sta_batchruntomo")
        number_processed += 1

        end_time = time.time()  # Stop measuring the time for this iteration
        processing_time = end_time - start_time
        minutes, seconds = divmod(processing_time, 60)
        print(f"Done. {directory.name} took {int(minutes)} min {int(seconds)} sec.")
        # Report how long the job has been running
        current_time = time.time() - init_time
        minutes, seconds = divmod(current_time, 60)
        print(f"{number_found + number_processed} of {number_to_process} completed.")
        print(f"Total time elapsed: {int(minutes)} min {int(seconds)} sec")
        # Report how long the job is expected to run
        expected_time = (number_to_process - number_found) / (number_processed / current_time)
        minutes, seconds = divmod(expected_time, 60)
        print(f"Total time expected: {int(minutes)} min {int(seconds)} sec")
        print("----")