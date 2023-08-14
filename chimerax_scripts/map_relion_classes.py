from pathlib import Path
import pandas as pd
import numpy as np

data_star = './run_it025_data.star'

column_labels = [
    'CoordinateX', #1 
    'CoordinateY', #2 
    'CoordinateZ', #3 
    'AngleRot', #4 
    'AngleTilt', #5 
    'AnglePsi', #6 
    'MicrographName', #7 
    'Magnification', #8 
    'DetectorPixelSize', #9 
    'CtfMaxResolution', #10 
    'ImageName', #11 
    'CtfImage', #12 
    'PixelSize', #13 
    'Voltage', #14 
    'SphericalAberration', #15 
    'GroupNumber', #16 
    'OriginX', #17 
    'OriginY', #18 
    'OriginZ', #19 
    'ClassNumber', #20 
    'NormCorrection', #21 
    'LogLikeliContribution', #22 
    'MaxValueProbDistribution', #23 
    'NrOfSignificantSamples', #24 
]

data = pd.read_csv(data_star, delim_whitespace=True, names=column_labels, skiprows=28)

for row in range(len(data)):
    classNumber = data['ClassNumber'].iloc[row]
    micrograph = data['MicrographName'].iloc[row]
    filename = f"class{classNumber}_{Path(micrograph).stem}.star"
    filepath = Path(filename)
    
    if filepath.is_file() == False:
        with open(filepath,'w') as file:
            with open(data_star) as star:
                head = [next(star) for x in range(28)]
            file.write("".join(str(item) for item in head))
    
    with open(filepath,'a') as file:
        row_to_write = "\t".join(str(item) for item in data.iloc[row].tolist())
        file.write(row_to_write)
        file.write("\n")
        file.close()


