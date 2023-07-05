import click
import subprocess
import time
import pandas as pd
from pathlib import Path
import starfile

from ..utils import *
from .sta_defoci import sta_defoci


def sta_isonet_setup(
    data_directory,
    working_directory,
    project_name: str,
    pixel_size: float,
) -> Path:
    data_directory = Path(data_directory).absolute()
    working_directory = Path(working_directory).absolute()

    ts_defoci_dict = sta_defoci(data_directory)

    isonet_star_df = pd.DataFrame()
    isonet_star_df["rlnIndex"] = range(len(ts_defoci_dict))
    isonet_star_df["rlnMicrographName"] = ts_defoci_dict.keys()
    isonet_star_df["rlnPixelSize"] = pixel_size
    isonet_star_df["rlnDefocus"] = ts_defoci_dict.values()
    isonet_star_df["rlnNumberSubtomo"] = 60

    isonet_star_file = working_directory / f"{project_name}.star"

    starfile.write(isonet_star_df, isonet_star_file, overwrite=True)

    return isonet_star_file


# def sta_isonet_deconv(
#    isonet_star_file: Path,
#    project_name: str,
#    voltage: int,
#    cs: float,
#    snr_falloff: float,
#    deconv_strength: float,
#    n_cpu: int,
#    tomogram_idx_list,
# ) -> None:
#    isonet_star_file = Path(isonet_star_file).absolute()
#    command = [
#        "isonet.py",
#        "deconv",
#        isonet_star_file,
#        "--deconv_folder",
#        deconv_folder,
#        "--voltage",
#        voltage,
#        "--cs",
#        cs,
#        "--snrfalloff",
#        snr_falloff,
#        "--deconvstrength",
#        deconv_strength,
#        "--highpassnyquist",
#        highpass_nyquist,
#        "--ncpu",
#        n_cpu,
#        "--tomo_idx"
#        tomogram_idx_list,
#    ]
#
# def sta_isonet_mask(
#    isonet_star_file: Path,
#    project_name: str,
#    density_percentage: float,
#    std_percentage: float,
#    z_crop: float,
#    tomogram_idx_list
# ) -> None:
#    isonet_star_file = Path(isonet_star_file).absolute()
#    command = [
#    	"isonet.py",
#        "make_mask",
#        isonet_star_file,
#        "--mask_folder",
#        mask_folder,
# 		"--density_percentage",
#        density_percentage,
#        "--std_percentage",
#        std_percentage,
# 		"--z_crop",
#        z_crop,
#        "--tomo_idx",
#        tomogram_idx_list,
#    ]
#
# def sta_isonet_extract(
#    isonet_star_file: Path,
#    tomogram_idx_list,
# ):
#    isonet_star_file = Path(isonet_star_file).absolute()
#
#    command = [
#        "isonet.py",
#        "extract",
#        isonet_star_file,
#        "--subtomo_folder",
#        subtomo_folder,
# 	    "--subtomo_star",
#        subtomo_star_file,
#        "--cube_size",
#        cube_size,
#        "--crop_size",
#        crop_size,
#        "--tomo_idx",
#        tomogram_idx_list,
#    ]
#
# def sta_isonet_refine(
#    isonet_star_file: Path,
#    iterations: int,
#    gpu_ids,
# ):
#    isonet_star_file = Path(isonet_star_file).absolute()
#    command = [
#        "isonet.py",
#        "refine",
#        subtomo_star_file,
#        "--gpuID",
#        gpu_ids,
#        "--iterations",
#        iterations,
#        "--result_dir",
#        result_directory,
#        "--log_level",
#        log_level,
#        "--data_dir",
#        data_directory,
#        "--noise_level",
#        noise_level,
#        "--noise_start_iter",
#        noise_start_iter,
#        "--learning_rate",
#        learning_rate,
#        "--drop_out",
#        drop_out,
#        "--kernel",
#        kernel,
#        "--unet_depth",
#        unet_depth,
#    ]
#
# def sta_isonet_predict(
#    isonet_star_file: Path,
#    gpu_ids,
# ):
#    isonet_star_file = Path(isonet_star_file).absolute()
#    isonet.py predict $STAR_FILE $TRAINED_MODEL --output_dir $OUTPUT_DIR --gpuID $GPUID \
# 		--cube_size $CUBE_SIZE_PREDICT --crop_size $CROP_SIZE_PREDICT #--tomo_idx $TOMO_IDX
#    command = [
#        "isonet.py",
#        'predict',
#        isonet_star_file,
#        trained_model,
#        '--output_dir',
#        output_directory,
#        '--gpuID',
#        gpu_ids,
#        '--cube_size',
#        cube_size,
#        '--crop_size',
#        crop_size,
#        '--tomo_idx',
#        tomogram_idx_list
#    ]


def sta_isonet(
    job: str,
    data_directory: Path,
    working_directory: Path,
    project_name: str,
    pixel_size: float,
) -> None:
    # choose 5 tomograms to train from, predict on all
    data_directory = Path(data_directory).absolute()
    working_directory = Path(working_directory).absolute()

    if job == "setup":
        sta_isonet_setup(data_directory, working_directory, project_name, pixel_size)
    # with open(directory / "sta_isonet.out", "a") as out, open(directory / "sta_isonet.err", "a") as err:
    #    result = subprocess.run(command, stdout=out, stderr=err)


@click.command()
@click.option(
    "--job",
    required=True,
    help='Name of the job to run. "setup", "deconv", "mask", "extract", "refine", "predict", or "all"',
)
@click.option(
    "--data_directory",
    "-data",
    required=True,
    help="The path to the directory containing all ts directories.",
)
@click.option(
    "--working_directory",
    "-working",
    default=".",
    help="The directory to output all isonet files.",
)
@click.option(
    "--project_name", "-name", default="isonet", help="The name of the project."
)
@click.option(
    "--pixel_size",
    "-ps",
    default="10.825",
    help="Pixel size in angstrom.",
)
def cli(
    job,
    data_directory,
    working_directory,
    project_name,
    pixel_size,
):
    sta_isonet(
        job,
        data_directory,
        working_directory,
        project_name,
        pixel_size,
    )
