from typer import Option
from pathlib import Path

from ..utilities.utils import *
from .._cli import cli, OPTION_PROMPT_KWARGS as PKWARGS

#from .alignframes import alignframes as _alignframes
from .alignframes_mp import alignframes_mp as _alignframes_mp
from .batchruntomo import batchruntomo as _batchruntomo
from .ctfplotter import ctfplotter as _ctfplotter

@cli.command(name="alignframes_mp", no_args_is_help=True)
def alignframes_mp(
    batch_directory: Path = Option(
        default=...,
        help="The path to the directory containing all ts directories.",
        **PKWARGS,
    ),
    align_binning: int = Option(
        default=1,
        help="Binning to be used for movie frame alignment.",
        **PKWARGS,
    ),
    sum_binning: int = Option(
        default=1,
        help="Binning to be used for movie frame summing. This will be the binning of the tilt series. Make sure to set the binning for the tomogram reconstruction accordingly. (e.g., setting bin=2 for reconstruction using a stack generated at --sum_binning=5 will result in a final binning of 10.",
        **PKWARGS,
    ),
    num_processes: int = Option(
        default=4,
        help="Number of parallel processes.",
        **PKWARGS,
    ),
) -> None:
    _alignframes_mp(batch_directory, align_binning, sum_binning, num_processes)

@cli.command(name="batchruntomo", no_args_is_help=True)
def batchruntomo(
    batch_directory: Path = Option(
        default=...,
        help="The path to the directory containing all ts directories.",
        **PKWARGS,
    ),
    directive_file: Path = Option(
        default=...,
        help="The path to the batchruntomo directive file.",
        **PKWARGS,
    ),
    n_cpus: int = Option(
        default=1,
        help="Number of parallel processes.",
        **PKWARGS,
    ),
    starting_step: float = Option(
        default=0,
        help="Starting step for batchruntomo.",
        **PKWARGS,
    ),
    ending_step: float = Option(
        default=20,
        help="Ending step for batchruntomo.",
        **PKWARGS,
    ),
    binning: int = Option(
        default=10,
        help="Binning to be used for movie frame alignment.",
        **PKWARGS,
    ),
    force: bool = Option(
        default=False,
        help="Force batchruntomo to run even if the success file is present.",
        **PKWARGS,
    ),
) -> None:
    _batchruntomo(batch_directory, directive_file, n_cpus, starting_step, ending_step, binning, force)

@cli.command(name="ctfplotter", no_args_is_help=True)
def ctfplotter(
    batch_directory: Path = Option(
        default=...,
        help="The path to the directory containing all ts directories.",
        **PKWARGS,
    ),
    axis_angle: float = Option(
        default=178.9,
        help="Tilt axis angle in degrees.",
        **PKWARGS,
    ),
    pixel_size: float = Option(
        default=1.0825,
        help="Pixel size in ångströms.",
        **PKWARGS,
    ),
) -> None:
    _ctfplotter(batch_directory, axis_angle, pixel_size)

@cli.command(name="full_preprocess", no_args_is_help=True)
def full_preprocess(
    batch_directory: Path = Option(
        default=...,
        help="The path to the directory containing all ts directories.",
        **PKWARGS,
    ),
    align_binning: int = Option(
        default=1,
        help="Binning to be used for movie frame alignment.",
        **PKWARGS,
    ),
    sum_binning: int = Option(
        default=1,
        help="Binning to be used for movie frame summing. This will be the binning of the tilt series. Make sure to set the binning for the tomogram reconstruction accordingly. (e.g., setting bin=2 for reconstruction using a stack generated at --sum_binning=5 will result in a final binning of 10.",
        **PKWARGS,
    ),
    n_procs_alignframes: int = Option(
        default=2,
        help="Number of parallel processes for alignframes.",
        **PKWARGS,
    ),
    directive_file: Path = Option(
        default=...,
        help="The path to the batchruntomo directive file.",
        **PKWARGS,
    ),
    n_cpus_batchruntomo: int = Option(
        default=4,
        help="Number of parallel processes for batchruntomo.",
        **PKWARGS,
    ),
    starting_step: float = Option(
        default=0,
        help="Starting step for batchruntomo.",
        **PKWARGS,
    ),
    ending_step: float = Option(
        default=20,
        help="Ending step for batchruntomo.",
        **PKWARGS,
    ),
    binning: int = Option(
        default=10,
        help="Binning to be used for movie frame alignment.",
        **PKWARGS,
    ),
    force: bool = Option(
        default=False,
        help="Force batchruntomo to run even if the success file is present.",
        **PKWARGS,
    ),
    axis_angle: float = Option(
        default=178.9,
        help="Tilt axis angle in degrees.",
        **PKWARGS,
    ),
    pixel_size: float = Option(
        default=1.0825,
        help="Pixel size in ångströms.",
        **PKWARGS,
    ),
) -> None:
    _alignframes_mp(batch_directory, align_binning, sum_binning, n_procs_alignframes)
    _batchruntomo(batch_directory, directive_file, n_cpus_batchruntomo, starting_step, ending_step, binning, force)
    _ctfplotter(batch_directory, axis_angle, pixel_size)