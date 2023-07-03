import subprocess
import click
from pathlib import Path
from typing import Optional
from ..utils import *


def sta_alignframes(
    mdoc_directory: Path, frames_directory: Path, align_binning: int, sum_binning: int
) -> None:
    mdoc_directory = Path(mdoc_directory).absolute()
    frames_directory = Path(frames_directory).absolute()

    ts_number = 1
    for mdoc in mdoc_directory.glob("*.mrc.mdoc"):
        """
        for each mrc.mdoc file describing a tilt series, create a subdirectory for the tilt series,
        align the movie frames, put them into a .st stack, move the stack and copy the mdoc into the
        tilt series subdirectory
        """
        if mdoc.stat().st_size < 10 * 1024:
            # if the mdoc file is bigger than 10 kB, to make sure it corresponds to a full tilt series
            print(
                "This mdoc doesn't seem to correspond to a tilt series. Skipping it..."
            )
            continue

        st_dir = Path(f"ts{ts_number:03}").absolute()
        output_image_file = st_dir / Path(f"ts{ts_number:03}.mrc")

        if not st_dir.exists():
            Path.mkdir(st_dir)

        # Check if this tilt stack has already been processed
        if check_job_success(st_dir):
            continue

        command = [
            "alignframes",
            "-MetadataFile",
            f"{mdoc}",
            "-PathToFramesInMdoc",
            frames_directory,
            "-OutputImageFile",
            output_image_file,
            "-binning",
            str(align_binning) + " " + str(sum_binning),
        ]

        with open(f"{st_dir.name}/sta_alignframes.out", "w") as out, open(
            f"{st_dir.name}/sta_alignframes.err", "w"
        ) as err:
            result = subprocess.run(command, stdout=out, stderr=err)

        # output_image_file.replace(output_image_file.with_suffix(f"_bin{align_binning}.st"))
        if int(align_binning) * int(sum_binning) > 1:
            output_image_file.rename(
                st_dir / (output_image_file.stem + f"_bin{int(sum_binning)}.mrc")
            )

        command = ["cp", mdoc.as_posix(), st_dir.as_posix()]
        result = subprocess.run(command)
        ts_number += 1
        job_success(st_dir, "sta_alignframes")


@click.command()
@click.option(
    "--mdoc_dir",
    "-mdoc",
    required=True,
    help="Path to the mdoc directory.",
)
@click.option(
    "--stack_dir",
    "-s",
    help="",
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
def cli(mdoc_dir, stack_dir, align_binning, sum_binning):
    if stack_dir == None:
        stack_dir = mdoc_dir + "/frames/"
    sta_alignframes(mdoc_dir, stack_dir, align_binning, sum_binning)
