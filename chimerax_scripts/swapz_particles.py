from pathlib import Path
from collections import OrderedDict

import starfile


def swapz_particles(
    star_file: Path,
    z_pixels: int,
):
    star_file = star_file.absolute()
    star_file_name = star_file.name

    star = starfile.read(star_file)
    print(star)
    if isinstance(star, OrderedDict):
        particles_star = star["particles"]
        optics_star = star["optics"]
    else:
        particles_star = star
        optics_star = None

    particles_star["rlnCoordinateZ"] = float(z_pixels) - particles_star["rlnCoordinateZ"]
    if optics_star is None:
        output_star = particles_star
    else:
        output_star = star
        output_star["particles"] = particles_star

    output_name = star_file.parent / f"swapz_{star_file_name}"
    starfile.write(particles_star, output_name, overwrite=True)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("star_file", type=Path)
    parser.add_argument("z_pixels", type=int)
    args = parser.parse_args()

    swapz_particles(
        star_file=args.star_file,
        z_pixels=args.z_pixels,
    )



