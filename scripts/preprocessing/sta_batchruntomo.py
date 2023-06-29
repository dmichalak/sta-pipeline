import click
import subprocess
from pathlib import Path
from .sta_fidder import sta_fidder
from ..utils import *

def sta_batchruntomo(directive_file, stack_dir, batch_dir, n_cpus, starting_step, ending_step, nofid, binning, fullnofid, pixel_spacing, probability_threshold):
    """
    """

    directive_file = Path(directive_file).absolute()
    if batch_dir is None and stack_dir is None: 
        print("Specifying either a batch directory (--batch_dir) or a single tilt series directory (--stack_dir) is required.")
        raise SystemExit(0)
    elif batch_dir is not None and stack_dir is not None: 
        print("Only *one* of either a batch directory (--batch_dir) or a single tilt series directory (--stack_dir) is required.")
        raise SystemExit(0)
    elif stack_dir is not None:
        stack_dir = Path(stack_dir).absolute()
        # check to make sure there is only one mrc file in the directory
        if starting_step == 0:
            mrc_file = [mrc for mrc in stack_dir.glob("*.mrc")]
            if len(mrc_file) != 1:
                print("There is either no or more than 1 .mrc file in the tilt series directory.")
                raise SystemExit(0)
            else:
                dirs_to_process = [stack_dir]
        else:
            dirs_to_process = [stack_dir]

    elif batch_dir is not None:
        batch_dir = Path(batch_dir).absolute()
        dirs_to_process = [dir for dir in batch_dir.glob("ts*")]
    else:
        print("Something has gone terribly wrong.")
        raise SystemExit(0)

    for directory in dirs_to_process:
        if "sta_batchruntomo.success" in check_job_success(directory):
            print(f"The file \"sta_batchruntomo.success\" was found. Skipping {directory.name}.")
            continue

        if fullnofid is False:
            rootname = f"{directory.parent.name}_{directory.name}_bin{binning}"

            if nofid == True and starting_step < 9:
                print("Using nofid is only meant for reconstruction steps.")
                raise SystemExit(0)
            elif nofid == True and starting_step >= 9:
                # rename aligned stacks so batchruntomo reconstructs a tomogram from the tilt series with fiducials erased
                aligned_stack_with_fiducials = directory / Path(rootname + "_ali.mrc")
                aligned_stack_without_fiducials = directory / Path(rootname + "_ali_nofid.mrc")
                aligned_stack_with_fiducials = aligned_stack_with_fiducials.rename(directory / Path(rootname + "_ali_fid.mrc"))
                aligned_stack_without_fiducials = aligned_stack_without_fiducials.rename(directory / Path(rootname + "_ali.mrc"))

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

            with open(f"batchruntomo_{directory.name}.log", "w") as log:
                        subprocess.run(command, stdout=log, stderr=log)
            
            aligned_stacks_renamed = False
            if nofid == True:
                aligned_stack_without_fiducials = aligned_stack_without_fiducials.rename(directory / Path(rootname + "_ali_nofid.mrc"))
                aligned_stack_with_fiducials = aligned_stack_with_fiducials.rename(directory / Path(rootname + "_ali.mrc"))
                aligned_stacks_renamed = True
            if nofid == True and aligned_stacks_renamed == False:
                print("WARNING: Aligned stacks were NOT renamed back to their original names.")
            job_success(directory, "sta_batchruntomo")
        else:
            if starting_step is None and ending_step is None:
                for directory in dirs_to_process:
                    rootname = f"{directory.parent.name}_{directory.name}_bin{binning}"
                    starting_step = 0
                    ending_step = 9

                    batchruntomo_command = [
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
                    with open(f"batchruntomo_{directory.name}.log", "w") as log:
                        subprocess.run(batchruntomo_command, stdout=log, stderr=log)

                    sta_fidder(directory / Path(rootname + "_ali.mrc"), directory, pixel_spacing, probability_threshold)

                    aligned_stack_with_fiducials = directory / Path(rootname + "_ali.mrc")
                    aligned_stack_without_fiducials = directory / Path(rootname + "_ali_nofid.mrc")
                    aligned_stack_with_fiducials = aligned_stack_with_fiducials.rename(directory / Path(rootname + "_ali_fid.mrc"))
                    aligned_stack_without_fiducials = aligned_stack_without_fiducials.rename(directory / Path(rootname + "_ali.mrc"))

                    starting_step = 10
                    ending_step = 20
                    batchruntomo_command = [
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
                    with open(f"batchruntomo_{directory.name}.log", "a") as log:
                        subprocess.run(batchruntomo_command, stdout=log, stderr=log)
                    aligned_stack_without_fiducials = aligned_stack_without_fiducials.rename(directory / Path(rootname + "_ali_nofid.mrc"))
                    aligned_stack_with_fiducials = aligned_stack_with_fiducials.rename(directory / Path(rootname + "_ali.mrc"))

                    nofid_sl_tomo = directory / Path(rootname + "_rec.mrc")
                    nofid_bp_tomo = directory / Path(rootname + "_rec_BP_rec.mrc")
                    nofid_sl_tomo = nofid_sl_tomo.rename(directory / Path(rootname + "_rec_nofid.mrc"))
                    nofid_bp_tomo = nofid_bp_tomo.rename(directory / Path(rootname + "_rec_BP_rec_nofid.mrc"))
                    job_success(directory, "sta_batchruntomo")
@click.command()
@click.option(
    "--directive_file",
    "-d",
    required=True,
    default=Path("directives.adoc"),
    help="The path to the .adoc file.",
)
@click.option("--stack_dir", "-td", default=None, help="The path to the directory of a single tilt series.")
@click.option("--batch_dir", "-bd", default=None, help="The path to the batch of tilt stacks, each in its own directory.")
@click.option("--n_cpus", "-n", default=2, help=".")
@click.option("--starting_step", "-s", default=None, help="""Step to end processing with in each set and axis.  Steps are numbered as... \
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
                 \n 22: Cleanup""")
@click.option("--ending_step", "-e", default=None, help=".")
@click.option("--nofid", "-nf", is_flag=True, help="Indicates that the tilt series with fiducials erased by fidder should be used.")
@click.option("--binning", "-bin", help="Indicate the binning, as defined in the directives.adoc,  of the aligned stack and any subsequent tomograms." )
@click.option("--fullnofid", is_flag=True, help="Process the tilt series from steps 0 to 20 and include fiducial erasing with fidder.")
@click.option("--pixel_spacing", "-ps", help="Pixel spacing for use with --nofid and --fullnofid.")
@click.option("--probability_threshold", "-pt", help="Probability threshold for use with --nofid and --fullnofid.")


def cli(directive_file, stack_dir, batch_dir, n_cpus, starting_step, ending_step, nofid, binning, fullnofid, pixel_spacing, probability_threshold):
    sta_batchruntomo(directive_file, stack_dir, batch_dir, n_cpus, starting_step, ending_step, nofid, binning, fullnofid, pixel_spacing, probability_threshold)
