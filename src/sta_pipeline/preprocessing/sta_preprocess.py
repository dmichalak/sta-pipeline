import subprocess
import click
from pathlib import Path
from typing import Optional

from ..utilities.utils import *
from . import sta_alignframes, sta_batchruntomo, sta_ctfplotter


def sta_preprocess(
    mdoc_directory: Path,
    align_binning: int,
    sum_binning: int,
    directive_file: Path,
    n_cpus: int,
    starting_step: float,
    ending_step: float,
    binning: int,
    axis_angle: float,
    pixel_size: float,
) -> None:
    pass


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
