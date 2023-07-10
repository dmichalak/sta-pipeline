from typer import Option

from ..utils import *
from .._cli import cli, OPTION_PROMPT_KWARGS as PKWARGS

from .eman2_predict import eman2_predict as _eman2_predict


@cli.command(name="eman2_predict", no_args_is_help=True)
def eman2_predict(
    trained_network = Option(
        default=...,
        help="The path to the trained network HDF file.",
        **PKWARGS,
    ),
    tomograms = Option(
        default=...,
        help="The path to the tomograms.",
        **PKWARGS,
    ),
) -> None:
    _eman2_predict(trained_network, tomograms)