from pathlib import Path
from typing import Optional
from typer import Option

from ..utils import *
from .._cli import cli, OPTION_PROMPT_KWARGS as PKWARGS

from .make_rln_tomo_star import make_rln_tomo_star as _make_rln_tomo_star

@cli.command(name="make_rln_tomo_star", no_args_is_help=True)
def make_rln_tomo_star(
    batch_directory: Path = Option(
        default=...,
        help="The path to the batch directory.",
        **PKWARGS,
    ),
    fractional_dose: float = Option(
        default=2.4,
        help="The fractional dose of the tilt series.",
        **PKWARGS,
    ),
) -> None:
    _make_rln_tomo_star(batch_directory, fractional_dose)