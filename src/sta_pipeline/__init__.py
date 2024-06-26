"""A subtomogram averaging pipeline."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("sta-pipeline")
except PackageNotFoundError:
    __version__ = "uninstalled"
__author__ = "Dennis J. Michalak"
__email__ = "dennis.michalak@nih.gov"


from ._cli import cli

from .preprocessing.cli import alignframes_mp, batchruntomo, ctfplotter, write_mdoc_to_ts_list
from .isonet.cli import isonet_setup, isonet_deconv, isonet_mask, isonet_extract, isonet_refine, isonet_predict
from .eman2.cli import eman2_predict, eman2_training, eman2_box_extract_mp
from .relion.cli import make_rln_tomo_star, rln_select_good_classes
from .utilities.cli import convert_star2tbl, convert_tbl2star
