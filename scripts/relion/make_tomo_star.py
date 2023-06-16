import pandas as pd

# Define the column names as a list
columns = [
    "_rlnTomoName",
    "_rlnTomoTiltSeriesName",
    "_rlnTomoImportCtfFindFile",
    "_rlnTomoImportImodDir",
    "_rlnTomoImportFractionalDose",
]

# Create the star file including the header
with open("tomograms_descr.star", "w") as f:
    f.write("# tomograms_descr.star\n\ndata_\n\nloop_\n")
    for column in columns:
        f.write(column + "\n")

# Create an empty DataFrame with the specified column names
df = pd.DataFrame(columns=columns)

# Save the DataFrame to a .star file in the current directory
df.to_csv("tomograms_descr.star", sep="\t", index=False, header=False, mode="a")
