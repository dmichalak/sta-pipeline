import click
import subprocess
from pathlib import Path
from ..utils import *

def sta_fidder(input_mrc, output_dir, pixel_spacing, probability_threshold):

    input_mrc = Path(input_mrc).absolute()
    output_dir = Path(output_dir).absolute()
    output_mask_name = input_mrc.stem + "_fidmask.mrc"
    output_mrc_name = input_mrc.stem + "_nofid.mrc"
    predict_command = [
        "fidder",
        "predict",
        "--input-image",
        input_mrc,
        "--pixel-spacing",
        pixel_spacing,
        "--probability-threshold",
        probability_threshold,
        "--output-mask",
        output_dir / output_mask_name,
    ]
    erase_command = [
        "fidder",
        "erase",
        "--input-image",
        input_mrc,
        "--input-mask",
        output_mask_name,
        "--output-image",
        output_dir / output_mrc_name,
    ]
    newstack_command = [
        "newstack",
        "-input",
        output_dir / output_mrc_name,
        "-output",
        output_dir / output_mrc_name,
        "-mode",
        "1"
    ]
    print("Starting prediction...")
    subprocess.run(predict_command)
    print("Starting erasing...")
    subprocess.run(erase_command)
    print("Converting the output .mrc from 32bit to 16bit...")
    subprocess.run(newstack_command)


@click.command()
@click.option(
    "--input",
    "-i",
    required=True,
    default=None,
    help="The input mrc stack to process.",
)
@click.option(
    "--output_dir",
    "-o",
    default=Path.cwd(),
    help="The output directory to write the masks and processed stack. Default = current directory",
)
@click.option(
    "--pixel_spacing",
    "-p",
    required=True, 
    default=None,
    help="Pixel spacing in Angstroms/px."
)
@click.option(
    "--probability_threshold",
    "-t",
    default=str(0.5),
    help="Probability threshold. Default = 0.5"
)

def cli(input, output_dir, pixel_spacing, probability_threshold):
    sta_fidder(input_mrc=input, output_dir=output_dir, pixel_spacing=pixel_spacing, probability_threshold=probability_threshold)