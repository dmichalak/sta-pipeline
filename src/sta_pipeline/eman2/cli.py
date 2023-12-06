from pathlib import Path
from typing import Optional
from typer import Option

from ..utilities.utils import *
from .._cli import cli, OPTION_PROMPT_KWARGS as PKWARGS

from .eman2_predict import eman2_predict as _eman2_predict
from .eman2_training import eman2_training as _eman2_training
from .eman2_box_extract_mp import eman2_box_extract_mp as _eman2_box_extract_mp


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
    gpu_id: Optional[int] = Option(
        default=0,
        help="The GPU ID to use for prediction.",
        **PKWARGS,
    ),
) -> None:
    _eman2_predict(trained_network, corrected_tomograms, gpu_id)

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
    gpu_id: Optional[int] = Option(
        default=0,
        help="The GPU ID to use for training.",
        **PKWARGS,
    ),
) -> None:
    _eman2_training(eman2_trainset, learning_rate, iterations, continue_from, gpu_id)

#@cli.command(name="eman2_box_extract", no_args_is_help=True)
#def eman2_box_extract(
#    eman2_directory = Option(
#        default=...,
#        help="The path to the directory containing the tomograms, segmentations, and info.",
#        **PKWARGS,
#    ),
#    tomo_bin_factor = Option(
#        default=...,
#        help="The binning factor of the segmented tomograms.",
#        **PKWARGS,
#    ),
#    box_size = Option(
#        default=...,
#        help="The size of the extracted boxes in pixels.",
#        **PKWARGS,
#    ),
#    feature_name = Option(
#        default=...,
#        help="The feature name for the extracted boxes.",
#        **PKWARGS,
#    ),
#    density_threshold = Option(
#        default=...,
#        help="The density threshold for peak extraction.",
#        **PKWARGS,
#    ),
#    mass_threshold = Option(
#        default=...,
#        help="The mass threshold for peak extraction.",
#        **PKWARGS,
#    ),
#) -> None:
#    _eman2_box_extract(eman2_directory, tomo_bin_factor, box_size, feature_name, density_threshold, mass_threshold)

@cli.command(name="eman2_box_extract_mp", no_args_is_help=True)
def eman2_box_extract_mp(
    eman2_directory = Option(
        default=...,
        help="The path to the directory containing the tomograms, segmentations, and info.",
        **PKWARGS,
    ),
    num_processes: int = Option(
        default=...,
        help="The number of processes to use for parallelization.",
        **PKWARGS,
    ),
    tomo_bin_factor = Option(
        default=...,
        help="The binning factor of the segmented tomograms.",
        **PKWARGS,
    ),
    box_size = Option(
        default=...,
        help="The size of the extracted boxes in pixels.",
        **PKWARGS,
    ),
    feature_name = Option(
        default=...,
        help="The feature name for the extracted boxes.",
        **PKWARGS,
    ),
    density_threshold = Option(
        default=...,
        help="The density threshold for peak extraction.",
        **PKWARGS,
    ),
    mass_threshold = Option(
        default=...,
        help="The mass threshold for peak extraction.",
        **PKWARGS,
    ),
) -> None:
    _eman2_box_extract_mp(eman2_directory, num_processes, tomo_bin_factor, box_size, feature_name, density_threshold, mass_threshold)
