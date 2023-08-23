from pathlib import Path

import time
import subprocess
import pandas as pd
from typer import Option
from os import PathLike
import starfile

from .get_defoci import sta_defoci
from ..utilities.utils import *
from .._cli import cli, OPTION_PROMPT_KWARGS as PKWARGS


#@cli.command(name="isonet_setup", no_args_is_help=True)
#def sta_isonet_setup(
#    data_directory: PathLike = Option(
#        default=...,
#        help="The path to the directory containing all ts directories.",
#        **PKWARGS,
#    ),
#    working_directory: PathLike = Option(
#        default=...,
#        help="The directory to output all isonet files.",
#        **PKWARGS,
#    ),
#    project_name: str = Option(
#        default="isonet",
#     None:arameters
#    ----------
#    data_directory : PathLike
#        The path to the directory containing all ts directories.
#    working_directory : PathLike
#        The directory to output all isonet files.
#    project_name : str
#        The name of the project.
#    pixel_size : float
#        The pixel size in angstrom.
#
#    Returns
#    -------
#    isonet_star_file : PathLike
#        The path to the star file.
#    """
#
#    data_directory = Path(data_directory).absolute()
#    working_directory = Path(working_directory).absolute()
#
#    # get the defocus values from the ctfplotter output files
#    ts_defoci_dict = sta_defoci(data_directory)
#
#    # create the a DataFrame for the star file
#    isonet_star_df = pd.DataFrame()
#    isonet_star_df["rlnIndex"] = range(1,len(ts_defoci_dict)+1)
#    isonet_star_df["rlnMicrographName"] = [f"{data_directory}/{ts_name}/{ts_name}_rec.mrc" for ts_name in ts_defoci_dict.keys()]
#    isonet_star_df["rlnPixelSize"] = pixel_size
#    isonet_star_df["rlnDefocus"] = ts_defoci_dict.values()
#    isonet_star_df["rlnNumberSubtomo"] = 60
#
#    # write the star file
#    isonet_star_filepath = working_directory / f"{project_name}.star"
#    starfile.write(isonet_star_df, isonet_star_filepath, overwrite=True)"


#@cli.command(name="isonet_deconv", no_args_is_help=True)
#def sta_isonet_deconv(
#    working_directory: PathLike = Option(
#        default=...,
#        help="The directory to output all isonet files.",
#        **PKWARGS,
#    ),
#    isonet_star_file: PathLike = Option(
#        default=...,
#        help="The path to the star file.",
#        **PKWARGS,
#    ),
#    project_name: str = Option(
#        default="isonet",
#        help="The name of the project.",
#        **PKWARGS,
#    ),
#    voltage: int = Option(
#        default=300,
#        help="The voltage of the microscope.",
#        **PKWARGS,
#    ),
#    cs: float = Option(
#        default=2.7,
#        help="The spherical aberration of the microscope in mm.",
#        **PKWARGS,
#    ),
#    snr_falloff: float = Option(
#        default=0.7,
#        help="The signal to noise ratio falloff.",
#        **PKWARGS,
#    ),
#    deconv_strength: float = Option(
#        default=1.0,
#        help="The deconvolution strength.",
#        **PKWARGS,
#    ),
#    n_cpu: int = Option(
#        default=4,
#        help="The number of CPUs to use.",
#        **PKWARGS,
#    ),
#    tomogram_idx_list: str = Option(
#        default="0,1,2,3,4",
#        help="The list of tomogram indices to use.",
#        **PKWARGS,
#    ),
# ) -> None:
#    """
#    Deconvolve the tilt series using isonet.
#    
#    Parameters
#    ----------
#    working_directory : PathLike
#        The directory to output all isonet files.
#    isonet_star_file : PathLike
#        The path to the star file.
#    project_name : str
#        The name of the project.
#    voltage : int
#        The voltage of the microscope.
#    cs : float
#        The spherical aberration of the microscope.
#    snr_falloff : float
#        The signal to noise ratio falloff.
#    deconv_strength : float
#        The deconvolution strength.
#    n_cpu : int
#        The number of CPUs to use.
#    tomogram_idx_list : list
#        The list of tomogram indices to use.
#
#    Returns
#    -------
#    None
#    """
#    
#    working_directory = Path(working_directory).absolute()
#    isonet_star_file = Path(isonet_star_file).absolute()
#
#    highpass_nyquist = 0.02
#
#    deconv_folder = working_directory / f"deconv_snr{snr_falloff}_{project_name}"
#    deconv_folder.mkdir(exist_ok=True)
#    command = [
#        "isonet.py",
#        "deconv",
#        f"{isonet_star_file}",
#        "--deconv_folder",
#        f"{deconv_folder}",
#        "--voltage",
#        f"{voltage}",
#        "--cs",
#        f"{cs}",
#        "--snrfalloff",
#        f"{snr_falloff}",
#        "--deconvstrength",
#        f"{deconv_strength}",
#        "--highpassnyquist",
#        f"{highpass_nyquist}",
#        "--ncpu",
#        f"{n_cpu}",
#        "--tomo_idx",
#        f"{tomogram_idx_list}",
#    ]
#    log_out = working_directory / "sta_isonet_deconv.out"
#    log_err = working_directory / "sta_isonet_deconv.err"
#    with open(log_out, "a") as out, open(log_err, "a") as err:
#        result = subprocess.run(command, stdout=out, stderr=err)

#@cli.command(name="isonet_mask", no_args_is_help=True)
#def sta_isonet_mask(
#    working_directory: PathLike = Option(
#        default=...,
#        help="The directory to output all isonet files.",
#        **PKWARGS,
#    ),
#    isonet_star_file: PathLike = Option(
#        default=...,
#        help="The path to the star file.",
#        **PKWARGS,
#    ),
#    project_name: str = Option(
#        default="isonet",
#        help="The name of the project.",
#        **PKWARGS,
#    ),
#    density_percentage: int = Option(
#        default=50,
#        help="The density percentage.",
#        **PKWARGS,
#    ),
#    std_percentage: int = Option(
#        default=50,
#        help="The standard deviation percentage.",
#        **PKWARGS,
#    ),
#    z_crop: float = Option(
#        default=0.1,
#        help="The z crop.",
#        **PKWARGS,
#    ),
#    tomogram_idx_list: str = Option(
#        default="0,1,2,3,4",
#        help="The list of tomogram indices to use.",
#        **PKWARGS,
#    ),
# ) -> None:
#    """
#    Create the mask for isonet.
#
#    Parameters
#    ----------
#    working_directory : PathLike
#        The directory to output all isonet files.
#    isonet_star_file : PathLike
#        The path to the star file.
#    project_name : str
#        The name of the project.
#    density_percentage : float
#        The density percentage.
#    std_percentage : float
#        The standard deviation percentage.
#    z_crop : float
#        The z crop.
#    tomogram_idx_list : list
#        The list of tomogram indices to use.
#
#    Returns
#    -------
#    None
#    """
#    working_directory = Path(working_directory).absolute()
#    isonet_star_file = Path(isonet_star_file).absolute()
#    mask_folder = working_directory / f"mask_dp{density_percentage}sp{std_percentage}_{project_name}"
#
#    """ 
#    patch_size: The size of the box from which the max-filter and std-filter are calculated
#
#    From IsoNet_v).2_Tutorial.md: "Since this demo tomogram has a bin-factor of 4, 
#    a smaller Gaussian filter can smooth out noise and keep the fine structure. We set patch_size to 2." 
#    patch_size = 2 was for 18.6 A/px, so for 10.825 A/px, we use patch_size = 4
#    """
#    patch_size = 4
#
#    command = [
#    	"isonet.py",
#        "make_mask",
#        f"{isonet_star_file}",
#        "--mask_folder",
#        f"{mask_folder}",
# 		"--density_percentage",
#        f"{density_percentage}",
#        "--std_percentage",
#        f"{std_percentage}",
# 		"--z_crop",
#        f"{z_crop}",
#        "--patch_size",
#        f"{patch_size}",
#        "--tomo_idx",
#        f"{tomogram_idx_list}",
#    ]
#
#    log_out = working_directory / "sta_isonet_mask.out"
#    log_err = working_directory / "sta_isonet_mask.err"
#    with open(log_out, "a") as out, open(log_err, "a") as err:
#        result = subprocess.run(command, stdout=out, stderr=err)

@cli.command(name="isonet_extract", no_args_is_help=True)
def isonet_extract(
    working_directory: PathLike = Option(
        default=...,
        help="The directory to output all isonet files.",
        **PKWARGS,
    ),
    project_name: str = Option(
        default="isonet",
        help="The name of the project.",
        **PKWARGS,
    ),
    isonet_star_file: PathLike = Option(
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
        default="0,1,2,3,4",
        help="The list of tomogram indices to use.",
        **PKWARGS,
    ),
):
    working_directory = Path(working_directory).absolute()
    isonet_star_file = Path(isonet_star_file).absolute()
    subtomo_folder = f"subtomo_dp{density_percentage}sp{std_percentage}_{project_name}"
    subtomo_star_file = f"subtomo_dp{density_percentage}sp{std_percentage}_{project_name}.star"
    cube_size = 64
    crop_size = 64 + 16

    command = [
        "isonet.py",
        "extract",
        f"{isonet_star_file}",
        "--subtomo_folder",
        f"{subtomo_folder}",
	    "--subtomo_star",
        f"{subtomo_star_file}",
        "--cube_size",
        f"{cube_size}",
        "--crop_size",
        f"{crop_size}",
        "--tomo_idx",
        f"{tomogram_idx_list}",
    ]

    log_out = working_directory / "sta_isonet_extract.out"
    log_err = working_directory / "sta_isonet_extract.err"
    with open(log_out, "a") as out, open(log_err, "a") as err:
        result = subprocess.run(command, stdout=out, stderr=err)

@cli.command(name="isonet_refine", no_args_is_help=True)
def isonet_refine(
    working_directory: PathLike = Option(
        default=...,
        help="The directory to output all isonet files.",
        **PKWARGS,
    ),
    scratch_directory: PathLike = Option(
        default=...,
        help="The temporary directory used for training.",
        **PKWARGS,
    ),
    subtomo_star_file: PathLike = Option(
        default=...,
        help="The path to the star file.",
        **PKWARGS,
    ),
    project_name: str = Option(
        default="isonet",
        help="The name of the project.",
        **PKWARGS,
    ),
    gpu_ids: str = Option(
        default="0",
        help="The GPU IDs to use.",
        **PKWARGS,
    ),
    n_cpu: int = Option(
        default=4,
        help="The number of CPUs to use.",
        **PKWARGS,
    ),
    iterations: int = Option(
        default=30,
        help="The number of iterations to train for.",
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
):
    working_directory = Path(working_directory).absolute()
    scratch_directory = Path(scratch_directory).absolute()
    subtomo_star_file = Path(subtomo_star_file).absolute()
    result_directory = working_directory / f"refine_dp{density_percentage}sp{std_percentage}_{project_name}"

    log_level = ""
    noise_level = "0.05,0.1,0.15,0.2"
    noise_start_iter = "11,16,21,26"
    learning_rate = "0.0004"
    drop_out = "0.3"
    kernel = "(3,3,3)"
    unet_depth = "3"

    command = [
        "isonet.py",
        "refine",
        f"{subtomo_star_file}",
        "--gpuID",
        f"{gpu_ids}",
        "--preprocessing_ncpus",
        f"{n_cpu}",
        "--iterations",
        f"{iterations}",
        "--result_dir",
        f"{result_directory}",
        "--log_level",
        f"{log_level}",
        "--data_dir",
        f"{scratch_directory}",
        "--noise_level",
        f"{noise_level}",
        "--noise_start_iter",
        f"{noise_start_iter}",
        "--learning_rate",
        f"{learning_rate}",
        "--drop_out",
        f"{drop_out}",
        "--kernel",
        f"{kernel}",
        "--unet_depth",
        f"{unet_depth}",
    ]

    log_out = working_directory / "sta_isonet_refine.out"
    log_err = working_directory / "sta_isonet_refine.err"
    with open(log_out, "a") as out, open(log_err, "a") as err:
        result = subprocess.run(command, stdout=out, stderr=err)

@cli.command(name="isonet_predict", no_args_is_help=True)
def isonet_predict(
    project_name: str = Option(
        default="isonet",
        help="The name of the project.",
        **PKWARGS,
    ),
    isonet_star_file: PathLike = Option(
        default=...,
        help="The path to the star file.",
        **PKWARGS,
    ),
    refine_directory: PathLike = Option(
        default=...,
        help="The path to the refine directory.",
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
    tomogram_idx_list: str = Option(
        default="0,1,2,3,4",
        help="The list of tomogram indices to use.",
        **PKWARGS,
    ),
):
    isonet_star_file = Path(isonet_star_file).absolute()
    refine_directory = Path(refine_directory).absolute()
    trained_model = refine_directory / "model_iter30.h5"
    output_directory = refine_directory / ".." / f"predict_dp{density_percentage}sp{std_percentage}_{project_name}"
    cube_size = 64
    crop_size = 64 + 16

    command = [
        "isonet.py",
        'predict',
        f"{isonet_star_file}",
        f"{trained_model}",
        '--output_dir',
        f"{output_directory}",
        '--gpuID',
        f"{gpu_ids}",
        '--cube_size',
        f"{cube_size}",
        '--crop_size',
        f"{crop_size}",
        '--tomo_idx',
        f"{tomogram_idx_list}",
    ]

    log_out = refine_directory / ".." / "sta_isonet_predict.out"
    log_err = refine_directory / ".." / "sta_isonet_predict.err"
    with open(log_out, "a") as out, open(log_err, "a") as err:
        result = subprocess.run(command, stdout=out, stderr=err)


def sta_isonet(
    job: str,
    project_name: str,
    working_directory: PathLike,
    scratch_directory: PathLike,
    data_directory: PathLike,
    isonet_star_file: PathLike,
    pixel_size: float,
    voltage: int,
    cs: float,
    snr_falloff: float,
    deconv_strength: float,
    n_cpu: int,
    density_percentage: int,
    std_percentage: int,
    z_crop: float,
    subtomo_star_file: PathLike,
    refine_directory: PathLike,
    gpu_ids: str,
    iterations: int,
    tomogram_idx_list,
) -> None:
    # choose 5 tomograms to train from, predict on all
    working_directory = Path(working_directory).absolute()
    data_directory = Path(data_directory).absolute()

    if job == "setup":
        sta_isonet_setup(data_directory, working_directory, project_name, pixel_size)

    elif job == "deconv":
        sta_isonet_deconv(
            working_directory,
            isonet_star_file,
            project_name,
            voltage,
            cs,
            snr_falloff,
            deconv_strength,
            n_cpu,
            tomogram_idx_list,
        )
    elif job == "mask":
        sta_isonet_mask(
            working_directory,
            isonet_star_file,
            project_name,
            density_percentage,
            std_percentage,
            z_crop,
            tomogram_idx_list,
        )
    elif job == "extract":
        sta_isonet_extract(
            working_directory,
            project_name,
            isonet_star_file,
            density_percentage,
            std_percentage,
            tomogram_idx_list,
        )
    elif job == "refine":
        sta_isonet_refine(
            working_directory,
            scratch_directory,
            subtomo_star_file,
            project_name,
            gpu_ids,
            n_cpu,
            iterations,
            density_percentage,
            std_percentage,
        )
    elif job == "predict":
        sta_isonet_predict(
            project_name,
            isonet_star_file,
            refine_directory,
            density_percentage,
            std_percentage,
            gpu_ids,
            tomogram_idx_list,
        )
    elif job == "all":
        sta_isonet_setup(data_directory, working_directory, project_name, pixel_size)
        sta_isonet_deconv(
            working_directory,
            isonet_star_file,
            project_name,
            voltage,
            cs,
            snr_falloff,
            deconv_strength,
            n_cpu,
            tomogram_idx_list,
        )
        sta_isonet_mask(
            working_directory,
            isonet_star_file,
            project_name,
            density_percentage,
            std_percentage,
            z_crop,
            tomogram_idx_list,
        )
        sta_isonet_extract(
            working_directory,
            project_name,
            isonet_star_file,
            density_percentage,
            std_percentage,
            tomogram_idx_list,
        )
        sta_isonet_refine(
            working_directory,
            scratch_directory,
            subtomo_star_file,
            project_name,
            gpu_ids,
            iterations,
            density_percentage,
            std_percentage,
        )
        sta_isonet_predict(
            project_name,
            isonet_star_file,
            refine_directory,
            density_percentage,
            std_percentage,
            gpu_ids,
            tomogram_idx_list,
        )




@click.command()
@click.option(
    "--job",
    required=True,
    help='Name of the job to run. "setup", "deconv", "mask", "extract", "refine", "predict", or "all"',
)
@click.option(
    "--project_name", "-name", default="isonet", help="The name of the project."
)
@click.option(
    "--working_directory",
    "-working",
    default=".",
    show_default=True,
    help="The directory to output all isonet files.",
)
@click.option(
    "--data_directory",
    "-data",
    default="../tomograms",
    help="The path to the directory containing all ts directories.",
)
@click.option(
    "--isonet_star_file",
    "-star",
    default=None,
    help="The path to the star file.",
)
@click.option(
    "--pixel_size",
    "-ps",
    default="10.825",
    show_default=True,
    help="Pixel size in angstrom.",
)
@click.option(
    "--voltage",
    "-v",
    default="300",
    show_default=True,
    help="The voltage of the microscope.",
)
@click.option(
    "--cs",
    "-cs",
    default="2.7",
    show_default=True,
    help="The spherical aberration of the microscope in mm.",
)
@click.option(
    "--snr_falloff",
    "-snr",
    default="0.7",
    show_default=True,
    help="The signal to noise ratio falloff.",
)
@click.option(
    "--deconv_strength",
    "-deconv",
    default="1.0",
    show_default=True,
    help="The deconvolution strength.",
)
@click.option(
    "--n_cpu",
    "-n",
    default="4",
    show_default=True,
    help="The number of CPUs to use.",
)
@click.option(
    "--density_percentage",
    "-dp",
    default="50",
    show_default=True,
    help="The density percentage.",
)
@click.option(
    "--std_percentage",
    "-sp",
    default="50",
    show_default=True,
    help="The standard deviation percentage.",
)
@click.option(
    "--z_crop",
    "-z",
    default="0.1",
    show_default=True,
    help="The z crop.",
)
@click.option(
    "--subtomo_star_file",
    "-subtomo",
    default=None,
    help="The path to the subtomo star file.",
)
@click.option(
    "--scratch_directory",
    "-scratch",
    default=None,
    help="The path to the scratch directory.",
)
@click.option(
    "--refine_directory",
    "-refine",
    default=None,
    help="The path to the refine directory.",
)
@click.option(
    "--gpu_ids",
    "-gpu",
    default="0",
    show_default=True,
    help="The GPU IDs to use.",
)
@click.option(
    "--iterations",
    "-iter",
    default="30",
    show_default=True,
    help="The number of iterations to use.",
)
@click.option(
    "--tomogram_idx_list",
    "-tomos",
    default="0,1,2,3,4",
    show_default=True,
    help="The list of tomogram indices to use.",
)


def cli(
    job: str,
    project_name: str,
    working_directory: PathLike,
    scratch_directory: PathLike,
    data_directory: PathLike,
    isonet_star_file: PathLike,
    pixel_size: float,
    voltage: int,
    cs: float,
    snr_falloff: float,
    deconv_strength: float,
    n_cpu: int,
    density_percentage: int,
    std_percentage: int,
    z_crop: float,
    subtomo_star_file: PathLike,
    refine_directory: PathLike,
    gpu_ids: str,
    iterations: int,
    tomogram_idx_list: str,
):
    sta_isonet(
        job,
        project_name,
        working_directory,
        scratch_directory,
        data_directory,
        isonet_star_file,
        pixel_size,
        voltage,
        cs,
        snr_falloff,
        deconv_strength,
        n_cpu,
        density_percentage,
        std_percentage,
        z_crop,
        subtomo_star_file,
        refine_directory,
        gpu_ids,
        iterations,
        tomogram_idx_list,
    )
