import click
import subprocess
import os                                                                                     
from pathlib import Path
from contextlib import contextmanager

@contextmanager
def cd(path):
    """Changes working directory and returns to previous on exit."""
    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)

    return

cwd_path = Path.cwd().absolute()

def sta_batchruntomo(directivefile, batchdir, numcpus, startingstep, endingstep, alignbinning, st_dir=None):
    """
    """
    batchdir_path = Path(batchdir).absolute()
    if st_dir is not None:
        st_dir = Path(st_dir)
    with cd(batchdir_path):
        if st_dir == None:
            for st_dir in Path().glob("ts*"):
                stack_rootname = None
                for stack in st_dir.glob("*.st"):
                    if stack_rootname is not None:
                        print("There is more than one .st file in the stack directory.")
                        raise SystemExit(0)
                    stack_rootname = stack.stem
    
                command = [
                    "batchruntomo",
                    "-DirectiveFile",
                    cwd_path / directivefile, 
                    "-RootName",
                    #f"{batchdir_path.name}_{st_dir}",
                    f"{stack_rootname}",
                    "-CurrentLocation",
                    f"{st_dir.absolute()}",
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
                    # "-MakeSubDirectory",
                    "-MakeComExtensionPcm",
                    "0",
                ]
                with open(f"batchruntomo_{batchdir_path.name}_{st_dir}.log", "w") as log:
                    subprocess.run(command, stdout=log, stderr=log)
                for rec in st_dir.glob("*rec*.mrc"):
                    rec.rename( st_dir / Path(rec.stem + f"_bin{alignbinning}" + rec.suffix))
        else:
                command = [
                    "batchruntomo",
                    "-DirectiveFile",
                    cwd_path / directivefile,
                    "-RootName",
                    f"{batchdir_path.name}_{st_dir}",
                    "-CurrentLocation",
                    f"{st_dir.absolute()}",
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
                    # "-MakeSubDirectory",
                    "-MakeComExtensionPcm",
                    "0",
                ]
                with open(f"batchruntomo_{batchdir_path.name}_{st_dir}.log", "w") as log:
                    subprocess.run(command, stdout=log, stderr=log) 
                for rec in st_dir.glob("*rec*.mrc"):
                    rec.rename( st_dir / Path(rec.stem + f"_bin{alignbinning}" + rec.suffix))

@click.command()
@click.option(
    "--directivefile",
    "-d",
    required=True,
    default=cwd_path/Path("directives.adoc"),
    help="The path to the .adoc file.",
)
@click.option("--batchdir", "-b", required=True, help="The path to the aligned stacks.")
@click.option("--numcpus", "-n", default=2, help=".")
@click.option("--ctf", is_flag=True, help=".")
@click.option("--startingstep", "-s", default=0, help="""Step to end processing with in each set and axis.  Steps are
              numbered as follows:
                 0: Setup
                 1: Preprocessing
                 2: Cross-correlation alignment
                 3: Prealigned stack
                 4: Patch tracking, autoseeding, or RAPTOR
                 5: Bead tracking
                 6: Alignment
                 7: Positioning
                 8: Aligned stack generation
                 9: CTF plotting
                 10: 3D gold detection
                 11: CTF correction
                 12: Gold erasing after transforming fiducial model or
                     projecting 3D model
                 13: 2D filtering
                 14: Reconstruction
                 14.5: Postprocessing on a/b axis reconstruction
                 15: Combine setup
                 16: Solvematch
                 17: Initial matchvol
                 18: Autopatchfit
                 19: Volcombine
                 20: Postprocessing with Trimvol
                 21: NAD (Nonlinear anistropic diffusion)
                 22: Cleanup""")
@click.option("--endingstep", "-e", default=20, help=".")
@click.option("--alignbinning", "-bin", help="Indicate the binning, as defined in the directives.adoc,  of the aligned stack and any subsequent tomograms." )
@click.option("--stackdir", "-sd", help=".")


def cli(directivefile, batchdir, numcpus, ctf, startingstep, endingstep, alignbinning, stackdir):
    if not ctf:
        sta_batchruntomo(directivefile, batchdir, numcpus, startingstep, endingstep, alignbinning, stackdir)
    else:
        sta_batchruntomo(directivefile, batchdir, numcpus, 9, 9, alignbinning, stackdir)
