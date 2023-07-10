# Adapted from https://github.com/teamtomo/fidder

"""A subtomogram averaging pipeline."""
from importlib.metadata import PackageNotFoundError, version

__version__ = "0.1" #version("sta_pipeline")

__author__ = "Dennis J. Michalak"
__email__ = "dennis.michalak@nih.gov"

__all__ = ["__version__", "cli"]

from ._cli import cli
# cli tools
from .preprocessing.cli import alignframes, alignframes_mp, batchruntomo, ctfplotter
from .isonet.cli import isonet_setup, isonet_deconv, isonet_mask, isonet_extract, isonet_refine, isonet_predict
# python things

