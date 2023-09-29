from pathlib import Path

from chimerax.core.commands import run


tomogram_directory = Path('/mnt/scratch/ribosomes/kas_k44a/eman2/mrcs').absolute()


run(session, "artiax start")
run(session, "hide #1.1 models")

tomo_index = 0
for tomogram in sorted(tomogram_directory.glob('ts*b10_rec.mrc')):
    tomo_index += 1
    run(session, f"artiax open tomo {tomogram.absolute().as_posix()}")
    run(session, f"hide #1.1.{tomo_index} models")

run(session, "volume #1.1 showOutline true")
pen