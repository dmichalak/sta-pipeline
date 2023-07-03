from pathlib import Path

batch_dir = Path("/media/michalakdj/scratch/data/wws1")

for ts_dir in batch_dir.glob("ts*"):
    for defoci_file in ts_dir.glob("*.defocus"):
        with open(defoci_file) as f:
            for line in f.readlines():
                line_split = line.split("\t")
                # print(line_split)
                if line_split[0] == "26":  # the 26th tilt frame in a series, 0deg tilt
                    print(
                        f"The 26th frame of {defoci_file.name}, tilt angle = {line_split[2]}, has defoci of {line_split[4]} nm and {line_split[5]}, mean defocus = {(float(line_split[4])+float(line_split[5]))/2} nm. \n"
                    )
