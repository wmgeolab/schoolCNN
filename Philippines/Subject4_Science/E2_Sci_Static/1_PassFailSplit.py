import pandas as pd
import shutil
import os

# Read in the data
df = pd.read_csv("./Philippines/Subject4_Science/E2_Sci_Static/data/y1314_Science.csv")
df.head()

# Set up the base directory
directory = "./Philippines/Subject4_Science/E2_Sci_Static/data/imagery/"

for filename in os.listdir(directory):
    # The firt 6 characters in the file's path name are the school's unique ID number
    schoolID = filename[0:6]
    # Use the school's ID to subset the dataframe to that school
    subset = df[df['school_id'] == int(schoolID)]
    # Construct the name of the file that will be copied into the pass or fail folder
    fname = directory + filename
    # If the school's intervention value is 1, move it into the fail folder (the school scored below average on the NAT)
    if subset['intervention'].tolist()[0] == 1:
        shutil.copy(fname, "./Philippines/Subject4_Science/E2_Sci_Static/data/fail/")
    # If the school's intervention value is 0, move it into the pass folder (the school scored above average on the NAT)
    if subset['intervention'].tolist()[0] == 0:
        shutil.copy(fname, "./Philippines/Subject4_Science/E2_Sci_Static/data/pass/")
