import pandas as pd
import shutil
import os

# Read in the data
df = pd.read_csv("./Brazil/E1_Landsat/data/y15_Brazil.csv")
df.head()

# Set up the base directory
directory = "./Brazil/E3_StreetView/data/imagery/"

for filename in os.listdir(directory):
    schoolID = filename[0:8]
    subset = df[df['school_id'] == int(schoolID)]
    fname = directory + filename
    if subset['intervention'].tolist()[0] == 1:
        shutil.copy(fname, "./Brazil/E3_StreetView/data/fail/")
    if subset['intervention'].tolist()[0] == 0:
        shutil.copy(fname, "./Brazil/E3_StreetView/data/pass/")