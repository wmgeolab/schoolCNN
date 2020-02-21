import pandas as pd
import random
import shutil
import math
import os

coords = pd.read_csv("./Philippines/Subject1_English/E1_Eng_Landsat/data/y1314_AllSubjects.csv")

pass_files = os.listdir("./Philippines/Subject1_English/E1_Eng_Landsat/data/pass/")
fail_files = os.listdir("./Philippines/Subject1_English/E1_Eng_Landsat/data/fail/")

pass_length = len(pass_files)
fail_length = len(fail_files)

TrainPassNum = math.ceil(pass_length * .75)
TrainFailNum = math.ceil(fail_length * .75)
ValPassNum = pass_length - TrainPassNum
ValFailNum = fail_length - TrainFailNum

TrainPass = random.sample(pass_files, TrainPassNum)
TrainFail = random.sample(fail_files, TrainFailNum)
ValPass = list(set(pass_files) - set(TrainPass))
ValFail = list(set(fail_files) - set(TrainFail))


for filename in TrainPass:
    fName = "./Philippines/Subject1_English/E1_Eng_Landsat/data/pass/" + filename
    shutil.copy(fName, "./Philippines/Subject1_English/E1_Eng_Landsat/data/train/pass/")

for filename in TrainFail:
    fName = "./Philippines/Subject1_English/E1_Eng_Landsat/data/fail/" + filename
    shutil.copy(fName, "./Philippines/Subject1_English/E1_Eng_Landsat/data/train/fail")

for filename in ValPass:
    fName = "./Philippines/Subject1_English/E1_Eng_Landsat/data/pass/" + filename
    shutil.copy(fName, "./Philippines/Subject1_English/E1_Eng_Landsat/data/val/pass")

for filename in ValFail:
    fName = "./Philippines/Subject1_English/E1_Eng_Landsat/data/fail/" + filename
    shutil.copy(fName, "./Philippines/Subject1_English/E1_Eng_Landsat/data/val/fail")