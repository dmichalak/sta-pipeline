from pathlib import Path

from chimerax.core.commands import run

tomogram_directory = Path('/mnt/storage/data/kas_k44a/ribosomes_21tomos').absolute()
i=0
for tomogram in sorted(tomogram_directory.glob('ts_02*/ts*b10_rec.mrc')):
    # if i < 4 run, if not stop
    run(session, f"hide #!1.1 models")
    run(session, f"artiax open tomo {tomogram.absolute().as_posix()}")
    run(session, f"hide #!1.1 models")




run(session, 'volume #1.1 showOutline true')