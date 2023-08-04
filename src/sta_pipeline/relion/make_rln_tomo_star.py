from pathlib import Path
import pandas as pd

import starfile


def make_rln_tomo_star(
    batch_directory: Path,
    fractional_dose: float,
) -> None:
    
    batch_directory = Path(batch_directory).absolute()

    # Define the column names as a list
    columns = [
        "rlnTomoName",
        "rlnTomoTiltSeriesName",
        "rlnTomoImportCtfFindFile",
        "rlnTomoImportImodDir",
        "rlnTomoImportFractionalDose",
        "rlnTomoImportOrderList"
    ]

    # Create an empty DataFrame with the columns defined above
    tomo_star_df = pd.DataFrame(columns=columns)

    # Find values for each of the columns
    rlnTomoName_list = []
    rlnTomoTiltSeriesName_list = []
    rlnTomoImportCtfFindFile_list = []
    rlnTomoImportImodDir_list = []
    rlnTomoImportFractionalDose_list = []
    rlnTomoImportOrderList_list = []

    # Print number of ts directories in batch directory
    print(f"Found {len(list(batch_directory.glob('ts*')))} tilt series directories.")

    for ts_dir in sorted(batch_directory.glob("ts*")):
        rlnTomoName_list.append(ts_dir.name)
        if ts_dir / f"{ts_dir.name}.mrc" in ts_dir.glob("*.mrc"):
            rlnTomoTiltSeriesName_list.append(f"tomograms/{ts_dir.name}/{ts_dir.name}.mrc")
        else:
            print(f"Error: {ts_dir.name}.mrc not found in {ts_dir}.")
            raise SystemExit(0)
        if ts_dir / f"{ts_dir.name}.defocus" in ts_dir.glob("*.defocus"):
            rlnTomoImportCtfFindFile_list.append(f"tomograms/{ts_dir.name}/{ts_dir.name}.defocus")
        else:
            print(f"Error: {ts_dir.name}.defocus not found in {ts_dir}.")
            raise SystemExit(0)
        rlnTomoImportImodDir_list.append(f"tomograms/{ts_dir.name}")
        rlnTomoImportFractionalDose_list.append(fractional_dose)
        rlnTomoImportOrderList_list.append("order_list.csv")

    # Add the lists to the DataFrame
    tomo_star_df["rlnTomoName"] = rlnTomoName_list
    tomo_star_df["rlnTomoTiltSeriesName"] = rlnTomoTiltSeriesName_list
    tomo_star_df["rlnTomoImportCtfFindFile"] = rlnTomoImportCtfFindFile_list
    tomo_star_df["rlnTomoImportImodDir"] = rlnTomoImportImodDir_list
    tomo_star_df["rlnTomoImportFractionalDose"] = rlnTomoImportFractionalDose_list
    tomo_star_df["rlnTomoImportOrderList"] = rlnTomoImportOrderList_list

    # Save the DataFrame as a star file
    starfile.write(tomo_star_df, "rln_tomo.star", overwrite=True)

    print(f"Successfully imported information from {len(tomo_star_df)} tilt series.")
    print(f"Saved rln_tomo.star in {Path.cwd()}.")

    