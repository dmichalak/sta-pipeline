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
from pathlib import Path
from ..utils import *


def sta_alignframes(batch_dir, stack_dir, align_binning, sum_binning):
    batch_dir_path = Path(batch_dir).absolute()
    stack_dir_path = Path(stack_dir).absolute()

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
                if check_job_success(st_dir):
                    continue
                output_image_file = st_dir / Path(f"{batch_dir_path.name}_ts{ts_number:03}.mrc")
                if not st_dir.exists():
                    Path.mkdir(st_dir)
                command = [
                    "alignframes",
                    "-MetadataFile",
                    f"{mdoc}",
                    "-PathToFramesInMdoc",
                    stack_dir_path.as_posix(),
                    "-OutputImageFile",
                    output_image_file.as_posix(),
                    "-binning",
                    str(align_binning)+" "+str(sum_binning),
                ]

                with open(f"{st_dir.name}/alignframes_{batch_dir_path.name}_ts{ts_number:03}.log","w") as log:
                    result = subprocess.run(command, stdout=log, stderr=log)

                #output_image_file.replace(output_image_file.with_suffix(f"_bin{align_binning}.st"))
                if int(align_binning) * int(sum_binning) > 1:
                    output_image_file.rename(st_dir / (output_image_file.stem + f"_bin{int(sum_binning)}.mrc"))
                command = [
                    "cp",
                    mdoc.as_posix(),
                    st_dir.as_posix()
                ]
                result = subprocess.run(command)
                ts_number += 1
                job_success(st_dir, "sta_alignframes")
@click.command()
@click.option(
    "--batch_dir",
    "-b",
    required=True,
    help="Path to the batch directory.",
)
@click.option(
    "--stack_dir",
    "-f",
    help="",
)
@click.option(
    "--align_binning",
    "-ab",
    default=5,
    help="Binning to be used for movie frame alignment."
)
@click.option(
    "--sum_binning",
    "-sb",
    default=5,
    help="Binning to be used for movie frame summing. This will be the binning of the tilt series. Make sure to set the binning for the tomogram reconstruction accordingly. (e.g., setting bin=2 for reconstruction using a stack generated at --sum_binning=5 will result in a final binning of 10."
)

def cli(batch_dir, stack_dir, align_binning, sum_binning):
    if stack_dir == None:
        stack_dir = batch_dir + "/frames/"
    sta_alignframes(batch_dir, stack_dir, align_binning, sum_binning)
