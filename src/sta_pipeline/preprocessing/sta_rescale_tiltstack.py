import click
import subprocess
from pathlib import Path
from ..utils import *
import mrcfile


def sta_rescale_tiltstack(
    input_stack: Path,
    output_stack: Path,
    output_pixel_size: float,
    bin_factor: float,
    n_cpus: int,
) -> None:
    input_stack = Path(input_stack).absolute()
    output_stack = Path(output_stack).absolute()

    with mrcfile.open(input_stack) as mrc:
        voxel_size = mrc.voxel_size
    if bin_factor is None:
        bin_factor = float(output_pixel_size) / voxel_size.x
        pixelsize = f"{output_pixel_size},{output_pixel_size},{output_pixel_size}"
    else:
        new_apix = voxel_size.x * float(bin_factor)
        pixelsize = f"{new_apix},{new_apix},{new_apix}"

    command = [
        "relion_tomo_bin_stack",
        "--i",
        f"{input_stack}",
        "--o",
        f"{output_stack}",
        "--bin",
        f"{bin_factor}",
        "--j",
        f"{n_cpus}",
    ]
    result = subprocess.run(command)
    command = [
        "alterheader",
        f"{output_stack}",
        "-PixelSize",
        f"{pixelsize}",
    ]
    result = subprocess.run(command)


@click.command()
@click.option(
    "--input_stack",
    "-i",
    required=True,
    help="Help text",
)
@click.option(
    "--output_stack",
    "-o",
    required=True,
    help="Help text",
)
@click.option(
    "--output_pixel_size",
    "-apix",
    help="Help text",
)
@click.option(
    "--bin_factor",
    "-bin",
    help="Help text",
)
@click.option(
    "--n_cpus",
    "-n",
    default=1,
    show_default=True,
    help="Help text",
)
def cli(input_stack, output_stack, output_pixel_size, bin_factor, n_cpus):
    sta_rescale_tiltstack(
        input_stack, output_stack, output_pixel_size, bin_factor, n_cpus
    )
