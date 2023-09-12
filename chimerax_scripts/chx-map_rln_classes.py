from pathlib import Path

from chimerax.core.commands import run



classification_directory = Path('/mnt/scratch/ribosomes/kas_k44a/relion/Class3D/b4_cl2_lp70A_K10').absolute()


run(session, "artiax start")
classes_dict = {}

# Get the particle positions and subtomogram averages for each class
for class_mrc in sorted(classification_directory.glob('run_it025_class*.mrc')):
    class_number = int(class_mrc.stem.split('class')[-1][0:3])
    classes_dict[class_number] = {}
    classes_dict[class_number]["mrc"] = class_mrc
    classes_dict[class_number]["data"] = classification_directory / f"class{class_number:03}_it025_data.star"


list_index = 1
for class_number in classes_dict.keys():
    if classes_dict[class_number]["data"].is_file():
        run(session, f"open {classes_dict[class_number]['data'].absolute()} format star")
        run(session, f"open {classes_dict[class_number]['mrc']}")
        run(session, f"artiax attach #2 toParticleList #1.2.{list_index}")
        run(session, f"volume #1.2.{list_index}.1.1 capFaces false")
        run(session, f"artiax show #1.2.{list_index} surfaces")
        run(session, f"hide #1.2.{list_index} models")

        list_index += 1



run(session, "artiax particles #1.2 originScaleFactor 1.0825")
run(session, "artiax particles #1.2 axesSize 0.1")