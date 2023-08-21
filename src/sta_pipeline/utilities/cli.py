from pathlib import Path
from typer import Option
from typing import Optional

from ..utils import *
from .._cli import cli, OPTION_PROMPT_KWARGS as PKWARGS

from .convert_star2tbl import convert_star2tbl as _convert_star2tbl
from .convert_tbl2star import convert_tbl2star as _convert_tbl2star

@cli.command(name="convert_star2tbl", no_args_is_help=True)
def convert_star2tbl(
    input_directory: str = Option(
        default=...,
        help="The path to the directory containing the star files. By default, the output directory is the same as the input directory. \n Note: To match RELION-v4.0's convention, all star files will use unbinned coordinates. Dynamo generally expects coordinates to match the binning of the corresponding tomogram in tbl files and, therefore, can vary.",
        **PKWARGS,
    ),
    input_binning: int = Option(
        default=1,
        help="The binning of the coordinates in the input star files.",
        **PKWARGS,
    ),
    output_binning: int = Option(
        default=...,
        help="The desired binning of the coordinates in the output tbl files.",
        **PKWARGS,
    ),
    overwrite: Optional[bool] = Option(
        default=False,
        help="Overwrite existing tbl files.",
        **PKWARGS,
    ),
) -> None:
    _convert_star2tbl(input_directory, input_binning, output_binning, overwrite)


@cli.command(name="convert_tbl2star", no_args_is_help=True)
def convert_tbl2star(
    input_directory: str = Option(
        default=...,
        help="The path to the directory containing the tbl files. By default, the output directory is the same as the input directory. \n Note: RELION-v4.0 generally expects coordinates to be unbinned in star files. Dynamo generally expects coordinates to match the binning of the corresponding tomogram in tbl files.",
        **PKWARGS,
    ),
    input_binning: int = Option(
        default=1,
        help="The binning of the coordinates in the input tbl files.",
        **PKWARGS,
    ),
    ts_directories: Path = Option(
        default=...,
        help="The path to the directory containing all of the tilt series directories.",
        **PKWARGS,
    ),
    overwrite: Optional[bool] = Option(
        default=False,
        help="Overwrite existing star files.",
        **PKWARGS,
    ),
) -> None:
    _convert_tbl2star(input_directory, input_binning, ts_directories, overwrite)