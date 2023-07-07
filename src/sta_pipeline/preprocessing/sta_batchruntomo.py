import click
import subprocess
import time
from pathlib import Path
from ..utils import *


def sta_batchruntomo(
    input_directory: Path,
    directive_file: Path,
    n_cpus: int,
    starting_step: float,
    ending_step: float,
    binning: int,
    force: bool,
) -> None:
    # Look for the "frames" and "mdoc" directories
    input_directory = Path(input_directory).absolute()
    directive_file = Path(directive_file).absolute()

    frames_directory = input_directory / "frames"
    mdoc_directory = input_directory / "mdoc"
    if frames_directory.is_dir() and mdoc_directory.is_dir():
        print(
            f"Found 'frames' and 'mdoc' directories: processing all tilt series within {input_directory}..."
        )
        dirs_to_process = [dir for dir in input_directory.glob("ts*")]
    # Look for a .mrc in input_directory
    elif (
        Path(input_directory / f"{input_directory}.mrc").is_file()
        or Path(input_directory / f"{input_directory}_bin{binning}.mrc").is_file()
    ):
        dirs_to_process = input_directory
    # If couldn't find either, exit script
    else:
        print(
            f"Error: Neither found 'frames' and 'mdoc' directories nor a stack to process in {input_directory}."
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
            "sta_batchruntomo.success" in check_job_success(directory)
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
            f"directive_file",
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


@click.command()
@click.option(
    "--input_directory",
    "-i",
    default=None,
    help="The path to the batch of tilt stacks, each in its own directory.",
)
@click.option(
    "--directive_file",
    "-d",
    required=True,
    default=Path("directives.adoc"),
    show_default=True,
    help="The path to the .adoc file.",
)
@click.option("--n_cpus", "-n", default=2, show_default=True,help=".")
@click.option(
    "--starting_step",
    "-s",
    default=None,
    help="""Processing step number to start with in batchruntomo. Steps are numbered as... \
                 \n 0: Setup
                 \n 1: Preprocessing
                 \n 2: Cross-correlation alignment
                 \n 3: Prealigned stack
                 \n 4: Patch tracking, autoseeding, or RAPTOR
                 \n 5: Bead tracking
                 \n 6: Alignment
                 \n 7: Positioning
                 \n 8: Aligned stack generation
                 \n 9: CTF plotting
                 \n 10: 3D gold detection
                 \n 11: CTF correction
                 \n 12: Gold erasing after transforming fiducial model or projecting 3D model
                 \n 13: 2D filtering
                 \n 14: Reconstruction
                 \n 15: Combine setup
                 \n 16: Solvematch
                 \n 17: Initial matchvol
                 \n 18: Autopatchfit
                 \n 19: Volcombine
                 \n 20: Postprocessing with Trimvol
                 \n 21: NAD (Nonlinear anistropic diffusion)
                 \n 22: Cleanup""",
)
@click.option(
    "--ending_step",
    "-e",
    default=None,
    help="Processing step number to end with in batchruntomo.",
)
@click.option(
    "--binning",
    "-bin",
    help="Indicate the binning, as defined in the directives.adoc,  of the aligned stack and any subsequent tomograms.",
)
@click.option(
    "--force",
    is_flag=True,
    default=False,
    help="Force processing even if sta_batchruntomo.success is found. BE CAREFUL!",
)
def cli(
    input_directory,
    directive_file,
    n_cpus,
    starting_step,
    ending_step,
    binning,
    force,
):
    sta_batchruntomo(
        input_directory,
        directive_file,
        n_cpus,
        starting_step,
        ending_step,
        binning,
        force,
    )
