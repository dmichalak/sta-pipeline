from pathlib import Path

from chimerax.core.commands import run

classification_directory = Path("/mnt/scratch/ribosomes/kas_k44a/relion/Class3D/b4_cl2_lp70A_K10")


def load_class_mrcs(
    classification_directory: Path,
):
    classification_directory = classification_directory.absolute()

    for class_average in sorted(classification_directory.glob("run_it025_class*.mrc")):
        run(session, f"open {class_average.absolute()}")

    run(session, "hide #* ")



load_class_mrcs(
    classification_directory=classification_directory,
)