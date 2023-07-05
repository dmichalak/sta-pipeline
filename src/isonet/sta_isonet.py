import click
import subprocess
import time
from pathlib import Path
from ..utils import *
from .sta_defoci import sta_defoci


def sta_isonet(
    input_directory: Path,
) -> None:
    input_directory = Path(input_directory).absolute()
    sta_defoci(input_directory)


@click.command()
@click.option(
    "--input_directory",
    "-i",
    default=None,
    help="The path to the batch of tilt stacks, each in its own directory.",
)

def cli(
    input_directory,
):
    sta_isonet(
        input_directory,
    )
