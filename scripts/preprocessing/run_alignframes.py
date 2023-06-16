#!/usr/env/bin python
"""
TO DO

[] - initialize ts_number = to the latest tilt stack number + 1
[] - 
       -path (-pat) OR -PathToFramesInMdoc      Text string
              Current path to the frame files listed in an ".mdoc" file, when
              these are being used as the input filenames.  If this option is
              not entered, the program must be run in the directory where the
              frames are located to access files listed in an ".mdoc" file.
"""
import subprocess
import click
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


def run_alignframes(batch_dir, frames_dir, align_binning, sum_binning):
    batch_dir_path = Path(batch_dir).absolute()
    frames_dir_path = Path(frames_dir).absolute()

    with cd(batch_dir_path):
        mdoc_dir = Path.cwd() / "mdoc"
        if not (mdoc_dir.exists() and mdoc_dir.is_dir()):
            mdoc_dir = Path.cwd()
        ts_number = 1
        for mdoc in mdoc_dir.glob("*.mrc.mdoc"):
            if mdoc.stat().st_size > 10 * 1024:  # if the mdoc file is bigger than 10 kB, to make sure it corresponds to a full tilt series
                """
                for each mrc.mdoc file describing a tilt series, create a subdirectory for the tilt series,
                align the movie frames, put them into a .st stack, move the stack and copy the mdoc into the
                tilt series subdirectory
                """
                output_image_file = Path(f"{batch_dir_path.name}_ts{ts_number:03}.mrc")
                st_dir = Path(f"ts{ts_number:03}").absolute()
                output_image_file = st_dir / Path(f"{batch_dir_path.name}_ts{ts_number:03}.mrc")
                if not st_dir.exists():
                    Path.mkdir(st_dir)
                command = [
                    "alignframes",
                    "-MetadataFile",
                    f"{mdoc}",
                    "-PathToFramesInMdoc",
                    frames_dir_path.as_posix(),
                    "-OutputImageFile",
                    output_image_file.as_posix(),
                    "-binning",
                    str(align_binning)+" "+str(sum_binning),
                ]

                with open(f"{st_dir.name}/alignframes_{batch_dir_path.name}_ts{ts_number:03}.log","w") as log:
                    result = subprocess.run(command, stdout=log, stderr=log)

                #output_image_file.replace(output_image_file.with_suffix(f"_bin{align_binning}.st"))
                if int(align_binning) * int(sum_binning) > 1:
                    output_image_file.rename(st_dir / (output_image_file.stem + f"_bin{int(align_binning) * int(sum_binning)}.st"))
                else:
                    output_image_file.rename(st_dir / (output_image_file.stem + f".st"))
                command = [
                    "cp",
                    mdoc.as_posix(),
                    st_dir.as_posix()
                ]
                result = subprocess.run(command)
                ts_number += 1
@click.command()
@click.option(
    "--batchdir",
    "-b",
    required=True,
    help="Path to the batch directory.",
)
@click.option(
    "--framesdir",
    "-f",
    help="",
)
@click.option(
    "--alignbinning",
    "-ab",
    default=5,
    help="Binning to be used for movie frame alignment."
)
@click.option(
    "--sumbinning",
    "-sb",
    default=5,
    help="Binning to be used for movie frame summing. This will be the binning of the tilt series. Make sure to set the binning for the tomogram reconstruction accordingly. (e.g., setting bin=2 for reconstruction using a stack generated at --sumbinning=5 will result in a final binning of 10."
)

def cli(batchdir, framesdir, alignbinning, sumbinning):
    if framesdir == None:
        framesdir = batchdir + "/frames/"
    run_alignframes(batchdir, framesdir, alignbinning, sumbinning)
