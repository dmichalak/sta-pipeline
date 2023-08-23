import click
import subprocess
from pathlib import Path
from ..utilities.utils import *


def function(var1, var2):

    return var1, var2


@click.command( help="Help text", show_default=True)
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
    function(option1, option2)
