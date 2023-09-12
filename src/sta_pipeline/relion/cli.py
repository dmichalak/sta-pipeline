from pathlib import Path
from typing import Optional
from typer import Option

from ..utilities.utils import *
from .._cli import cli, OPTION_PROMPT_KWARGS as PKWARGS

from .make_rln_tomo_star import make_rln_tomo_star as _make_rln_tomo_star
from .rln_select_good_classes import rln_select_good_classes as _rln_select_good_classes

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

@cli.command(name="rln_select_good_classes", no_args_is_help=True)
def rln_select_good_classes(
    classif_directory: Path = Option(
        default=...,
        help="The path to the directory containing the class_*.star files.",
        **PKWARGS,
    ),
    good_classes: str = Option(
        default=...,
        help="The list of good classes in the format '1,2,3,4,5'.",
        **PKWARGS,
    ),
    overwrite: Optional[bool] = Option(
        default=False,
        help="Whether to overwrite existing star files.",
        **PKWARGS,
    ),
) -> None:
    _rln_select_good_classes(classif_directory, good_classes, overwrite)