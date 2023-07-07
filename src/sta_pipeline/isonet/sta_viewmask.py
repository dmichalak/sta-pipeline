import click
from os import PathLike
from pathlib import Path
from skimage.io import imread
import mrcfile
import napari


def sta_viewmask(
    tomogram_directory: PathLike,
    mask_directory: PathLike
)-> None:
    """View the mask applied to the tomogram.

    Parameters
    ----------
    working_directory : PathLike
        Path to the working directory.
    mask_directory : PathLike  
        Path to the mask directory.
    """ 
    tomogram_directory = Path(tomogram_directory).absolute()    
    mask_directory = Path(mask_directory).absolute()

    viewer = napari.Viewer()
    masks = {}
    for mask in mask_directory.glob("*.mrc"):
        masks[mask.stem.split("_")[0]] = mrcfile.mmap(mask, permissive=True).data
        continue
    tomograms = {}
    for ts_name in masks.keys():
        tomograms[ts_name] = mrcfile.mmap(
            tomogram_directory / f"{ts_name}_rec.mrc", permissive=True).data
    
    masked_tomograms = {}
    for ts_name in masks.keys():
        masked_tomograms[ts_name] = tomograms[ts_name] * masks[ts_name]
        viewer.add_image(tomograms[ts_name], name=ts_name, visible=False)
        viewer.add_image(masked_tomograms[ts_name], name=f"{ts_name}_masked", visible=False)



@click.command()
@click.option(
    "--tomogram_directory",
    "-t",
    type=click.Path(exists=True),
    help="Path to the tomogram directory.",
)
@click.option(
    "--mask_directory",
    "-m",
    type=click.Path(exists=True),
    help="Path to the mask directory.",
)

def cli(
    tomogram_directory: PathLike,
    mask_directory: PathLike
):
    sta_viewmask(
        tomogram_directory=tomogram_directory,
        mask_directory=mask_directory
    )