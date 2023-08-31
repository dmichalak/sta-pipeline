from pathlib import Path

import pandas as pd

import starfile
from chimerax.core.commands import run

classification_directory = Path('/mnt/scratch/ribosomes/kas_k44a/relion/Class3D/bin8_cl1_K12T4_global').absolute()

# Get the particle positions for each ts
list_index = 1
for ts_star in sorted(classification_directory.glob('ts*.star')):
    run(session, f"open {ts_star.absolute()} format star")
    #run(session, f"open {classes_dict[class_number]['mrc']}")
    #run(session, f"artiax attach #2 toParticleList #1.2.{list_index}")
    #run(session, f"volume #1.2.{list_index}.1.1 capFaces false")
    #run(session, f"artiax show #1.2.{list_index} surfaces")
    run(session, f"hide #1.2.{list_index} models")

    list_index += 1


run(session, "artiax particles #1.2 originScaleFactor 1.0825")
run(session, "artiax particles #1.2 radius 50.0")
run(session, "artiax particles #1.2 axesSize 0.1")