from pathlib import Path

from chimerax.core.commands import run


tomogram_directory = Path('/mnt/storage/data/kas_k44a/ribosomes_21tomos').absolute()
run(session, "artiax start")
run(session, "hide #1.1 models")

tomo_index = 0
for tomogram in sorted(tomogram_directory.glob('ts*/ts*b10_rec.mrc')):
    tomo_index += 1
    run(session, f"artiax open tomo {tomogram.absolute().as_posix()}")
    run(session, f"hide #1.1.{tomo_index} models")

run(session, "volume #1.1 showOutline true")