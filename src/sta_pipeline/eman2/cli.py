from pathlib import Path
from typing import Optional
from typer import Option

from ..utilities.utils import *
from .._cli import cli, OPTION_PROMPT_KWARGS as PKWARGS

from .eman2_predict import eman2_predict as _eman2_predict
from .eman2_extract import eman2_extract as _eman2_extract
from .eman2_training import eman2_training as _eman2_training


@cli.command(name="eman2_predict", no_args_is_help=True)
def eman2_predict(
    trained_network= Option(
        default=...,
        help="The path to the trained network HDF file (ex: nnet_save__ribosomes_good.hdf).",
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
    segmentation_directory = Option(
        default=...,
        help="The path to the directory containing the tomograms and segmentations.",
        **PKWARGS,
    ),
    #neural_network = Option(
    #    default=...,
    #    help="The path to the trained network HDF file (ex: nnet_save__ribosomes_good.hdf).",
    #    **PKWARGS,
    #),
    tomo_bin_factor = Option(
        default=...,
        help="The binning factor of the segmented tomograms.",
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
    concatenate_star_files: Optional[bool] = Option(
        default=True,
        help="Whether to concatenate the star files into a single star file.",
        **PKWARGS,
    ),
) -> None:
    #_eman2_extract(segmentation_directory, neural_network, tomo_bin_factor, min_distance, rel_threshold, abs_threshold, concatenate_star_files)
    _eman2_extract(segmentation_directory, tomo_bin_factor, min_distance, rel_threshold, abs_threshold, concatenate_star_files)

@cli.command(name="eman2_training", no_args_is_help=True, )
def eman2_training(
    eman2_trainset: Path = Option(
        default=...,
        help="The path to the trainset HDF file.",
        **PKWARGS,
    ),
    learning_rate: float = Option(
        default=...,
        help="The learning rate for training.",
        **PKWARGS,
    ),
    iterations: int = Option(
        default=...,
        help="The number of iterations for training.",
        **PKWARGS,
    ),
    continue_from: Optional[Path] = Option(
        default=None,
        help="The path to a trained network HDF file to continue training from (ex. nnet_save__ribosomes_good.hdf).",
        **PKWARGS,
    ),
) -> None:
    _eman2_training(eman2_trainset, learning_rate, iterations, continue_from)