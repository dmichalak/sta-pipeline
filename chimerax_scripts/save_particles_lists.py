from pathlib import Path
import numpy as np

from chimerax.core.commands import run

particle_list_directory = Path('/mnt/scratch/ribosomes/kas_k44a/artiax_cleaning/bin6').absolute()
particle_list_namepattern = "ts_*_run_data"
particle_list_ext = "star"
pixel_size = 1.0825 #A/px

partlist_index_start = 11
partlist_index_end = 21
for i in np.arange(partlist_index_start, partlist_index_end+1):
    run(session, f"save {particle_list_directory}/artiax_ts_{str(i).zfill(3)}_run_data.star partlist #1.2.{i}")