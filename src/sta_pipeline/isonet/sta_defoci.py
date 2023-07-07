from pathlib import Path
import click


def sta_defoci(input_directory):
    """
    Get the defocus values from the ctfplotter output files.

    Parameters
    ----------
    input_directory : Path
        The path to the directory containing all ts directories.

    Returns
    -------
    ts_defocus_dict : dict
        A dictionary of ts names and defocus values.
    """
    input_directory = Path(input_directory).absolute()
    output_filepath = input_directory / f"{input_directory.name}.defocus"
    if output_filepath.is_file():
        output_filepath.rename(output_filepath.with_name(output_filepath.name + "~"))

    ts_defocus_dict= {}
    for ts_directory in sorted(input_directory.glob("ts*")):
        ts_directory = Path(ts_directory).absolute()
        defocus_filepath = Path(ts_directory / f"{ts_directory.name}.defocus")

        if defocus_filepath.is_file():
            with open(defocus_filepath) as defocus_file:
                ts_defocus_dict[ts_directory.name] = round(
                    sum(float(line.split("\t")[4]) + float(line.split("\t")[5]) for line in defocus_file if line.split("\t")[0] == "26") * 10 / 2,
                    1,
                )  # angstromm
        else:
            print(f"ERROR: Could not find {ts_directory.name}.defocus from ctfplotter.")
            with open(input_directory / "no_defocus.txt", "a") as f:
                f.write(ts_directory.name + "\n")

    with open(output_filepath, "a") as output_file:
        # write the mean defocus to a file 
        for ts, defocus in ts_defocus_dict.items():
            output_file.write(f"{ts}\t{defocus}\n")
    
    return ts_defocus_dict 



@click.command()
@click.option(
    "--input_directory",
    "-i",
    default=None,
    help="The path to the batch of tilt stacks, each in its own directory.",
)

def cli(
    input_directory,
):
    sta_defoci(
        input_directory,
    )
