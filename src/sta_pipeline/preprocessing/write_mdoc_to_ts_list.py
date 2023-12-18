from pathlib import Path
from typing import Optional

def write_mdoc_to_ts_list(
    batch_directory: Path,
    overwrite: Optional[bool] = False,
) -> None:
    """
    Write/append mdoc file name and ts_*** to a text file in the batch_directory

    Args:
        batch_directory (Path): Path to the batch directory
        overwrite (bool): Whether to overwrite existing mdoc_to_ts.txt file
    """
    batch_directory = Path(batch_directory).absolute()

    mdoc_to_ts_list = []
    for ts_directory in sorted(batch_directory.glob("ts*")):
        # Check if there is only one mdoc file in the ts_directory
        mdoc_files = list(ts_directory.glob("*.mrc.mdoc"))
        if len(mdoc_files) == 1:
            mdoc_to_ts_list.append([mdoc_files[0].name.split(".")[0], ts_directory.name])
        else:
            print(f"Error: Found {len(mdoc_files)} mdoc files in {ts_directory.name}.")
            raise SystemExit(0)
        
    # Sort the list by mdoc file name
    mdoc_to_ts_list.sort(key=lambda x: x[0])

    # Write to a text file in the batch_directory
    mdoc_to_ts_file = Path(batch_directory / "mdoc_to_ts.txt").absolute()

    if mdoc_to_ts_file.is_file() and overwrite == False:
        print(f"{mdoc_to_ts_file.name} already exists.")
        raise SystemExit(0)
    else:
        print(f"Writing {mdoc_to_ts_file.name}")
        with open(mdoc_to_ts_file, "w") as f:
            for mdoc_to_ts in mdoc_to_ts_list:
                f.write(f"{mdoc_to_ts[0]}\t{mdoc_to_ts[1]}\n")