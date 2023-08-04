from pathlib import Path

import pandas as pd
import starfile






def concat_star(
    starfile_directory: Path,
    output_star: Path,
) -> None:
    """Concatenate all star files in a directory into one star file."""

    starfile_directory = Path(starfile_directory).absolute()
    output_star = Path(output_star).absolute()

    starfile_list = []
    for star in sorted(starfile_directory.glob("*.star")):
        print(f"Reading {star.name}...")
        starfile_list.append(starfile.read(star))
    print("Concatenating star files...")
    concatenated_starfile = pd.concat(starfile_list, axis=1, ignore_index=True)
    print(f"Saving concatenated star file to {output_star}...")
    starfile.write(concatenated_starfile, output_star, overwrite=True)
    print("Done!")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Concatenate all star files in a directory into one star file."
    )
    parser.add_argument(
        "starfile_directory",
        type=Path,
        help="Directory containing star files to concatenate.",
    )
    parser.add_argument(
        "output_star",
        type=Path,
        help="Path to output concatenated star file.",
    )
    args = parser.parse_args()

    concat_star(
        args.starfile_directory,
        args.output_star,
    )