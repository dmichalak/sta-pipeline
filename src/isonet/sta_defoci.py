from pathlib import Path
import click


def sta_defoci(input_directory):
    input_directory = Path(input_directory).absolute()

    ts_defoci_dict = {}
    for ts_directory in input_directory.glob("ts*"):
        ts_directory = Path(ts_directory).absolute()
        defocus_file = Path(f"{ts_directory.name}.defocus").absolute()

        if defocus_file.is_file():
            with open(defocus_file) as def_file:
                # read the defoci and record the mean to a dictionary
                for line in def_file.readlines():
                    line_split = line.split("\t")
                    if line_split[0] == "26":
                        # mean defocus from the 2 defoci reported by ctfplotter
                        ts_defoci_dict[ts_directory.name] = (
                            (float(line_split[4]) + float(line_split[5])) * 10 / 2
                        )  # angstrom


        else:
            print(f"ERROR: Could not find {ts_directory.name}.defocus from ctfplotter.")
            with open(input_directory / "no_defocus.txt", "a") as f:
                f.write(ts_directory.name)
    with open(input_directory / f"{input_directory.name}.defocus", "a") as defoci_file:
        # write the mean defocus to a file 
        for ts, defocus in ts_defoci_dict:
            defoci_file.write(ts + "\t" + str(defocus) + "\n")
    
    return ts_defoci_dict



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
