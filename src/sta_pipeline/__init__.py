# Adapted from https://github.com/teamtomo/fidder

"""A subtomogram averaging pipeline."""
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("sta_pipeline")
except PackageNotFoundError:
    __version__ = "uninstalled"

__author__ = "Dennis J. Michalak"
__email__ = "dennis.michalak@nih.gov"

__all__ = ["__version__", "__author__", "__email__"]

from ._cli import cli
# cli tools
from .isonet import sta_isonet

# python things

