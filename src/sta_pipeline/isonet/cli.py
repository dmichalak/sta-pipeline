from typer import Option
from typing import Optional
from pathlib import Path

from ..utilities.utils import *
from .._cli import cli, OPTION_PROMPT_KWARGS as PKWARGS

from .isonet_setup import isonet_setup as _isonet_setup
from .isonet_deconv import isonet_deconv as _isonet_deconv
from .isonet_mask import isonet_mask as _isonet_mask
from .isonet_extract import isonet_extract as _isonet_extract
from .isonet_refine import isonet_refine as _isonet_refine
from .isonet_predict import isonet_predict as _isonet_predict


@cli.command(name="isonet_setup", no_args_is_help=True)
def isonet_setup(
    data_directory: Path = Option(
        default=...,
        help="The path to the directory containing all ts directories.",
        **PKWARGS,
    ),
    working_directory: Path = Option(
        default=".",
        help="The directory to output all isonet files.",
        **PKWARGS,
    ),
    project_name: str = Option(
        default="isonet",
        help="The name of the project. This will be used in naming subsequent files.",
        **PKWARGS,
    ),
    pixel_size: float = Option(
        default=...,
        help="The pixel size of the binned tomogram in ångströms.",
        **PKWARGS,
    ),
) -> None:
    _isonet_setup(data_directory, working_directory, project_name, pixel_size)


@cli.command(name="isonet_deconv", no_args_is_help=True)
def isonet_deconv(
    working_directory: Path = Option(
        default=".",
        help="The directory to output all isonet files.",
        **PKWARGS,
    ),
    isonet_star_file: Path = Option(
        default=...,
        help="The path to the star file.",
        **PKWARGS,
    ),
    project_name: str = Option(
        default="isonet",
        help="The name of the project.",
        **PKWARGS,
    ),
    voltage: int = Option(
        default=300,
        help="The voltage of the microscope in keV.",
        **PKWARGS,
    ),
    cs: float = Option(
        default=2.7,
        help="The spherical aberration of the microscope in mm.",
        **PKWARGS,
    ),
    snr_falloff: float = Option(
        default=0.7,
        help="The signal to noise ratio falloff. Start with 0.7 and adjust as needed between 0.5 and 1.0. Increasing this has previously improved results.",
        **PKWARGS,
    ),
    deconv_strength: float = Option(
        default=1.0,
        help="The deconvolution strength. Usually 1.0 is fine.",
        **PKWARGS,
    ),
    n_cpu: int = Option(
        default=4,
        help="The number of CPUs to use.",
        **PKWARGS,
    ),
    tomogram_idx_list: str = Option(
        default="1,2,3,4,5",
        help="The list of tomogram indices to use.",
        **PKWARGS,
    ),
) -> None:
    _isonet_deconv(working_directory, isonet_star_file, project_name, voltage, cs, snr_falloff, deconv_strength, n_cpu, tomogram_idx_list)


@cli.command(name="isonet_mask", no_args_is_help=True)
def isonet_mask(
    working_directory: Path = Option(
        default=".",
        help="The directory to output all isonet files.",
        **PKWARGS,
    ),
    isonet_star_file: Path = Option(
        default=...,
        help="The path to the star file.",
        **PKWARGS,
    ),
    project_name: str = Option(
        default="isonet",
        help="The name of the project.",
        **PKWARGS,
    ),
    density_percentage: int = Option(
        default=50,
        help="The density percentage. Start with 50 and adjust as needed between 0 and 100. Increasing this has previously improved results.",
        **PKWARGS,
    ),
    std_percentage: int = Option(
        default=50,
        help="The standard deviation percentage. Start with 50 and adjust as needed between 0 and 100. Increasing this has previously improved results.",
        **PKWARGS,
    ),
    z_crop: float = Option(
        default=0.2,
        help="The amount of the tomogram to mask on either side in the z-direction (e.g., z_crop = 0.2 means the top 20% and bottom 20% of the tomogram will be masked). ",
        **PKWARGS,
    ),
    tomogram_idx_list: str = Option(
        default="1,2,3,4,5",
        help="The list of tomogram indices to use.",
        **PKWARGS,
    ),
) -> None:
    _isonet_mask(working_directory, isonet_star_file, project_name, density_percentage, std_percentage, tomogram_idx_list)

@cli.command(name="isonet_extract", no_args_is_help=True)
def isonet_extract(
    working_directory: Path = Option(
        default=".",
        help="The directory to output all isonet files.",
        **PKWARGS,
    ),
    project_name: str = Option(
        default="isonet",
        help="The name of the project.",
        **PKWARGS,
    ),
    isonet_star_file: Path = Option(
        default=...,
        help="The path to the star file.",
        **PKWARGS,
    ),
    density_percentage: int = Option(
        default=50,
        help="The density percentage.",
        **PKWARGS,
    ),
    std_percentage: int = Option(
        default=50,
        help="The standard deviation percentage.",
        **PKWARGS,
    ),
    tomogram_idx_list: str = Option(
        default="1,2,3,4,5",
        help="The list of tomogram indices to use.",
        **PKWARGS,
    ),
) -> None:
    _isonet_extract(working_directory, project_name, isonet_star_file, density_percentage, std_percentage, tomogram_idx_list)


@cli.command(name="isonet_refine", no_args_is_help=True)
def isonet_refine(
    working_directory: Path = Option(
        default=".",
        help="The directory to output all isonet files.",
        **PKWARGS,
    ),
    scratch_directory: Path = Option(
        default=...,
        help="The directory to output scratch files.",
        **PKWARGS,
    ),
    subtomo_star_file: Path = Option(
        default=...,
        help="The path to the subtomogram star file.",
        **PKWARGS,
    ),
    project_name: str = Option(
        default="isonet",
        help="The name of the project.",
        **PKWARGS,
    ),
    gpu_ids: str = Option(
        default=...,
        help="The GPU IDs to use.",
        **PKWARGS,
    ),
    n_cpu: int = Option(
        default=4,
        help="The number of CPUs to use.",
        **PKWARGS,
    ),
    density_percentage: int = Option(
        default=50,
        help="The density percentage.",
        **PKWARGS,
    ),
    std_percentage: int = Option(
        default=50,
        help="The standard deviation percentage.",
        **PKWARGS,
    ),
) -> None:
    _isonet_refine(working_directory, scratch_directory, subtomo_star_file, project_name, gpu_ids, n_cpu, density_percentage, std_percentage)

@cli.command(name="isonet_predict", no_args_is_help=True)
def isonet_predict(
    project_name: str = Option(
        default="isonet",
        help="The name of the project.",
        **PKWARGS,
    ),
    isonet_star_file: Path = Option(
        default=...,
        help="The path to the star file.",
        **PKWARGS,
    ),
    refine_directory: Path = Option(
        default=".",
        help="The directory containing the output of IsoNet's \"refine\" job.",
        **PKWARGS,
    ),
    density_percentage: int = Option(
        default=50,
        help="The density percentage.",
        **PKWARGS,
    ),
    std_percentage: int = Option(
        default=50,
        help="The standard deviation percentage.",
        **PKWARGS,
    ),
    gpu_ids: str = Option(
        default="0",
        help="The GPU IDs to use.",
        **PKWARGS,
    ),
    tomogram_idx_list: Optional[str] = Option(
        default=None,
        help="The list of tomogram indices to use.",
    ),
) -> None:
    _isonet_predict(project_name, isonet_star_file, refine_directory, density_percentage, std_percentage, gpu_ids, tomogram_idx_list)


def isonet_full(
    data_directory: Path = Option(
        default=Path("../tomograms/"),
        help="The path to the directory containing all ts directories.",
        **PKWARGS,
    ),
    working_directory: Path = Option(
        default=".",
        help="The directory to output all isonet files.",
        **PKWARGS,
    ),
    project_name: str = Option(
        default="isonet",
        help="The name of the project.",
        **PKWARGS,
    ),
    pixel_size: float = Option(
        default=10.825,
        help="The pixel size in angstrom.",
        **PKWARGS,
    ),
    voltage: int = Option(
        default=300,
        help="The voltage of the microscope.",
        **PKWARGS,
    ),
    cs: float = Option(
        default=2.7,
        help="The spherical aberration of the microscope in mm.",
        **PKWARGS,
    ),
    snr_falloff: float = Option(
        default=0.7,
        help="The signal to noise ratio falloff.",
        **PKWARGS,
    ),
    deconv_strength: float = Option(
        default=1.0,
        help="The deconvolution strength.",
        **PKWARGS,
    ),
    n_cpu: int = Option(
        default=4,
        help="The number of CPUs to use.",
        **PKWARGS,
    ),
    density_percentage: int = Option(
        default=50,
        help="The density percentage.",
        **PKWARGS,
    ),
    std_percentage: int = Option(
        default=50,
        help="The standard deviation percentage.",
        **PKWARGS,
    ),
    gpu_ids: str = Option(
        default="0",
        help="The GPU IDs to use.",
        **PKWARGS,
    ),
    tomogram_idx_list: Optional[str] = Option(
        default=None,
        help="The list of tomogram indices to use.",
    ),
) -> None:
    
    isonet_star_file = _isonet_setup(data_directory, working_directory, project_name, pixel_size)
    _isonet_deconv(working_directory, isonet_star_file, project_name, voltage, cs, snr_falloff, deconv_strength, n_cpu, tomogram_idx_list)
    _isonet_mask(working_directory, isonet_star_file, project_name, density_percentage, std_percentage, tomogram_idx_list)
    _isonet_extract(working_directory, project_name, isonet_star_file, density_percentage, std_percentage, tomogram_idx_list)
    refine_directory = _isonet_refine(working_directory, project_name, isonet_star_file, density_percentage, std_percentage, tomogram_idx_list)
    _isonet_predict(project_name, isonet_star_file, refine_directory, density_percentage, std_percentage, gpu_ids, tomogram_idx_list
)