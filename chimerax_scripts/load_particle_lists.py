from pathlib import Path

from chimerax.core.commands import run

particle_list_directory = Path('/mnt/scratch/ribosomes/kas_k44a/eman2/segmentations').absolute()
particle_list_namepattern = "particles_ts_0*_abs0.1rel0.1_Xshift-10"
particle_list_ext = "star"
pixel_size = 1.0825 #A/px

for particle_list in sorted(
    particle_list_directory.glob(
        f'{particle_list_namepattern}.{particle_list_ext}'
        )
    ):
    run(session, f"open {particle_list_directory / particle_list} format {particle_list_ext}")

run(session, f"artiax particles #1.2 originScaleFactor {pixel_size}"
run(session, "artiax particles #1.2 axesSize 0.1")
run(session, "artiax particles #1.2 radius 50.0")