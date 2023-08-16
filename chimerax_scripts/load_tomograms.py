from pathlib import Path

from chimerax.core.commands import run

tomogram_directory = Path('/mnt/scratch/ribosomes/kas_k44a/eman2/tomos').absolute()

for tomogram in sorted(tomogram_directory.glob('ts_0*.mrc')):
    run(session, f"artiax open tomo {tomogram.absolute().as_posix()}")



run(session, 'volume #1.1 showOutline true')