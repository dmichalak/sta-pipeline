import subprocess
import time
from pathlib import Path
from ..utils import *

def fidder(
    batch_directory: Path,
    pixel_spacing: float,
    probability_threshold: float,

) -> None:
    
    batch_directory = Path(batch_directory).absolute()