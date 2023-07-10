# Adapted from https://github.com/teamtomo/fidder

"""A subtomogram averaging pipeline."""
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("sta_pipeline")
except PackageNotFoundError:
    __version__ = "uninstalled"

__author__ = "Dennis J. Michalak"
__email__ = "dennis.michalak@nih.gov"

__all__ = ["__version__", "cli"]

from ._cli import cli
# cli tools
from .isonet.isonet_setup import isonet_setup
from .isonet.isonet_deconv import isonet_deconv
from .isonet.isonet_mask import isonet_mask
from .isonet.isonet_extract import isonet_extract
from .isonet.isonet_refine import isonet_refine
from .isonet.isonet_predict import isonet_predict


# python things

