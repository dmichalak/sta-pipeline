import click
import subprocess
from pathlib import Path
from ..utils import *

def sta_eman2(var1, var2):
    return var1, var2

@click.command()
@click.option(
    "--option1",
    "-o1",
    required=True,
    default=None,
    help="Help text",
)
@click.option(
    "--option2",
    "-o2",
    required=True,
    default=None,
    help="Help text",
)

def cli(option1, option2):
    sta_eman2(option1, option2)