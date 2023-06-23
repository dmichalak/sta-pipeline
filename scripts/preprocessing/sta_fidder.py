import click
import subprocess
from pathlib import Path
from ..utils import *

def sta_fidder(input_stack, output_dir, pixel_spacing, probability_threshold):

    input_stack = Path(input_stack).absolute()
    output_dir = Path(output_dir).absolute()
    output_mask_name = input_stack.stem + "_fidmask.mrc"
    output_mrc_name = input_stack.stem + "_nofid.mrc"
    predict_command = [
        "fidder",
        "predict",
        "--input_stack-image",
        input_stack,
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
        "--input_stack-image",
        input_stack,
        "--input_stack-mask",
        output_mask_name,
        "--output-image",
        output_dir / output_mrc_name,
    ]
    newstack_command = [
        "newstack",
        "-input_stack",
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
    "--input_stack",
    "-i",
    required=True,
    default=None,
    help="The input_stack mrc stack to process.",
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

def cli(input_stack, output_dir, pixel_spacing, probability_threshold):
    sta_fidder(input_stack=input_stack, output_dir=output_dir, pixel_spacing=pixel_spacing, probability_threshold=probability_threshold)