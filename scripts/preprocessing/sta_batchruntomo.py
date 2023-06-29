import click
import subprocess
from pathlib import Path
from ..utils import *

def sta_batchruntomo(
        directive_file: Path,
        batch_dir: Path,
        n_cpus: int,
        starting_step: float,
        ending_step: float,
        binning: int,
        ) -> None:
    """
    """
    directive_file = directive_file.absolute()
    batch_dir = batch_dir.absolute()

    dirs_to_process = [dir for dir in batch_dir.glob("ts*")]

    for directory in dirs_to_process:
        if "sta_batchruntomo.success" in check_job_success(directory):
            print(f"The file \"sta_batchruntomo.success\" was found. Skipping {directory.name}.")
            continue

        rootname = f"{directory.parent.name}_{directory.name}_bin{binning}"

        command = [
            "batchruntomo",
            "-directive_file",
            directive_file, 
            "-RootName",
            rootname,
            "-CurrentLocation",
            f"{directory}",
            "-NamingStyle",
            "1",
            "-CPUMachineList",
            f"localhost:{n_cpus}",
            "-GPUMachineList",
            "1",
            "-starting_step",
            str(starting_step),
            "-ending_step",
            str(ending_step),
            "-MakeComExtensionPcm",
            "0",
        ]

        with open("sta_batchruntomo.out", "w") as out, open("sta_batchruntomo.err", "w") as err:
                    subprocess.run(command, stdout=out, stderr=err)
        job_success(directory, "sta_batchruntomo")


@click.command()
@click.option(
    "--directive_file",
    "-d",
    required=True,
    default=Path("directives.adoc"),
    help="The path to the .adoc file.",
    )
@click.option(
    "--batch_dir",
    "-bd",
    default=None,
    help="The path to the batch of tilt stacks, each in its own directory."
    )
@click.option(
    "--n_cpus",
    "-n",
    default=2,
    help="."
    )
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
                 \n 22: Cleanup"""
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

def cli(directive_file, batch_dir, n_cpus, starting_step, ending_step, binning,):
    sta_batchruntomo(directive_file, batch_dir, n_cpus, starting_step, ending_step, binning,)
