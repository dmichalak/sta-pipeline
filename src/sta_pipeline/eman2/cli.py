from typer import Option

from ..utils import *
from .._cli import cli, OPTION_PROMPT_KWARGS as PKWARGS

from .eman2_predict import eman2_predict as _eman2_predict
from .eman2_extract import eman2_extract as _eman2_extract


@cli.command(name="eman2_predict", no_args_is_help=True)
def eman2_predict(
    trained_network = Option(
        default=...,
        help="The path to the trained network HDF file.",
        **PKWARGS,
    ),
    corrected_tomograms = Option(
        default=...,
        help="The path to the tomograms \"corrected\" by IsoNet.",
        **PKWARGS,
    ),
) -> None:
    _eman2_predict(trained_network, corrected_tomograms)

@cli.command(name="eman2_extract", no_args_is_help=True)
def eman2_extract(
    eman2_directory = Option(
        default=...,
        help="The path to the directory containing the tomograms and segmentations.",
        **PKWARGS,
    ),
    min_distance = Option(
        default=...,
        help="The minimum distance between peaks in pixels.",
        **PKWARGS,
    ),
    rel_threshold = Option(
        default=...,
        help="The relative threshold for peak detection. The maximum of rel_threshold and abs_threshold is used.",
        **PKWARGS,
    ),
    abs_threshold = Option(
        default=...,
        help="The absolute threshold for peak detection. The maximum of rel_threshold and abs_threshold is used.",
        **PKWARGS,
    ),
) -> None:
    _eman2_extract(eman2_directory, min_distance, rel_threshold, abs_threshold)