import click
import subprocess
from pathlib import Path
from .sta_fidder import sta_fidder
from ..utils import *

def sta_batchruntomo(directivefile, tiltdir, batchdir, numcpus, startingstep, endingstep, nofid, binning, fullnofid, pixelspacing, probabilitythreshold):
    """
    """

    directivefile = Path(directivefile).absolute()
    if batchdir is None and tiltdir is None: 
        print("Specifying either a batch directory (--batchdir) or a single tilt series directory (--tiltdir) is required.")
        raise SystemExit(0)
    elif batchdir is not None and tiltdir is not None: 
        print("Only *one* of either a batch directory (--batchdir) or a single tilt series directory (--tiltdir) is required.")
        raise SystemExit(0)
    elif tiltdir is not None:
        tiltdir = Path(tiltdir).absolute()
        # check to make sure there is only one mrc file in the directory
        if startingstep == 0:
            mrc_file = [mrc for mrc in tiltdir.glob("*.mrc")]
            if len(mrc_file) != 1:
                print("There is either no or more than 1 .mrc file in the tilt series directory.")
                raise SystemExit(0)
            else:
                dirs_to_process = [tiltdir]
        else:
            dirs_to_process = [tiltdir]

    elif batchdir is not None:
        batchdir = Path(batchdir).absolute()
        dirs_to_process = [dir for dir in batchdir.glob("ts*")]
    else:
        print("Something has gone terribly wrong.")
        raise SystemExit(0)

    if fullnofid is False:
        for directory in dirs_to_process:
            rootname = f"{directory.parent.name}_{directory.name}_bin{binning}"

            if nofid == True and startingstep < 9:
                print("Using nofid is only meant for reconstruction steps.")
                raise SystemExit(0)
            elif nofid == True and startingstep >= 9:
                # rename aligned stacks so batchruntomo reconstructs a tomogram from the tilt series with fiducials erased
                aligned_stack_with_fiducials = directory / Path(rootname + "_ali.mrc")
                aligned_stack_without_fiducials = directory / Path(rootname + "_ali_nofid.mrc")
                aligned_stack_with_fiducials = aligned_stack_with_fiducials.rename(directory / Path(rootname + "_ali_fid.mrc"))
                aligned_stack_without_fiducials = aligned_stack_without_fiducials.rename(directory / Path(rootname + "_ali.mrc"))

            command = [
                "batchruntomo",
                "-DirectiveFile",
                directivefile, 
                "-RootName",
                rootname,
                "-CurrentLocation",
                f"{directory}",
                "-NamingStyle",
                "1",
                "-CPUMachineList",
                f"localhost:{numcpus}",
                "-GPUMachineList",
                "1",
                "-StartingStep",
                str(startingstep),
                "-EndingStep",
                str(endingstep),
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
    else:
        if startingstep is None and endingstep is None:
            for directory in dirs_to_process:
                rootname = f"{directory.parent.name}_{directory.name}_bin{binning}"
                startingstep = 0
                endingstep = 9

                batchruntomo_command = [
                    "batchruntomo",
                    "-DirectiveFile",
                    directivefile, 
                    "-RootName",
                    rootname,
                    "-CurrentLocation",
                    f"{directory}",
                    "-NamingStyle",
                    "1",
                    "-CPUMachineList",
                    f"localhost:{numcpus}",
                    "-GPUMachineList",
                    "1",
                    "-StartingStep",
                    str(startingstep),
                    "-EndingStep",
                    str(endingstep),
                    "-MakeComExtensionPcm",
                    "0",
                ]
                with open(f"batchruntomo_{directory.name}.log", "w") as log:
                    subprocess.run(batchruntomo_command, stdout=log, stderr=log)
                
                sta_fidder(directory / Path(rootname + "_ali.mrc"), directory, pixelspacing, probabilitythreshold)

                aligned_stack_with_fiducials = directory / Path(rootname + "_ali.mrc")
                aligned_stack_without_fiducials = directory / Path(rootname + "_ali_nofid.mrc")
                aligned_stack_with_fiducials = aligned_stack_with_fiducials.rename(directory / Path(rootname + "_ali_fid.mrc"))
                aligned_stack_without_fiducials = aligned_stack_without_fiducials.rename(directory / Path(rootname + "_ali.mrc"))

                startingstep = 10
                endingstep = 20
                batchruntomo_command = [
                    "batchruntomo",
                    "-DirectiveFile",
                    directivefile, 
                    "-RootName",
                    rootname,
                    "-CurrentLocation",
                    f"{directory}",
                    "-NamingStyle",
                    "1",
                    "-CPUMachineList",
                    f"localhost:{numcpus}",
                    "-GPUMachineList",
                    "1",
                    "-StartingStep",
                    str(startingstep),
                    "-EndingStep",
                    str(endingstep),
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
@click.command()
@click.option(
    "--directivefile",
    "-d",
    required=True,
    default=Path("directives.adoc"),
    help="The path to the .adoc file.",
)
@click.option("--tiltdir", "-td", default=None, help="The path to the directory of a single tilt series.")
@click.option("--batchdir", "-bd", default=None, help="The path to the batch of tilt stacks, each in its own directory.")
@click.option("--numcpus", "-n", default=2, help=".")
@click.option("--startingstep", "-s", default=None, help="""Step to end processing with in each set and axis.  Steps are numbered as... \
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
@click.option("--endingstep", "-e", default=None, help=".")
@click.option("--nofid", "-nf", is_flag=True, help="Indicates that the tilt series with fiducials erased by fidder should be used.")
@click.option("--binning", "-bin", help="Indicate the binning, as defined in the directives.adoc,  of the aligned stack and any subsequent tomograms." )
@click.option("--fullnofid", is_flag=True, help="Process the tilt series from steps 0 to 20 and include fiducial erasing with fidder.")
@click.option("--pixelspacing", "-ps", help="Pixel spacing for use with --nofid and --fullnofid.")
@click.option("--probabilitythreshold", "-pt", help="Probability threshold for use with --nofid and --fullnofid.")


def cli(directivefile, tiltdir, batchdir, numcpus, startingstep, endingstep, nofid, binning, fullnofid, pixelspacing, probabilitythreshold):
    sta_batchruntomo(directivefile, tiltdir, batchdir, numcpus, startingstep, endingstep, nofid, binning, fullnofid, pixelspacing, probabilitythreshold)
