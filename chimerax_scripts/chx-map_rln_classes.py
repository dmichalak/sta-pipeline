from pathlib import Path

import pandas as pd

import starfile
from chimerax.core.commands import run

classification_directory = Path('/mnt/scratch/ribosomes/kas_k44a/relion/Class3D/bin8_cl1_K12T4_global').absolute()







classes_dict = {}


# Get the particle positions and subtomogram averages for each class
for class_dir in sorted(classification_directory.glob('class*')):
    if class_dir.is_dir():
        class_number = int(class_dir.name[5:8])
        classes_dict[class_number] = {}
        classes_dict[class_number]["data"]= sorted(class_dir.glob("*.star"))
        #classes_dict[class_number]["mrc"] = classification_directory / f"run_it025_class{class_number:03}.mrc"


list_index = 1
for class_number in classes_dict.keys():
    for ts_star in classes_dict[class_number]["data"]:
        run(session, f"open {ts_star.absolute()} format star")
        #run(session, f"open {classes_dict[class_number]['mrc']}")
        #run(session, f"artiax attach #2 toParticleList #1.2.{list_index}")
        #run(session, f"volume #1.2.{list_index}.1.1 capFaces false")
        #run(session, f"artiax show #1.2.{list_index} surfaces")
        run(session, f"hide #1.2.{list_index} models")

        list_index += 1



run(session, "artiax particles #1.2 originScaleFactor 1.0825")
run(session, "artiax particles #1.2 axesSize 0.1")