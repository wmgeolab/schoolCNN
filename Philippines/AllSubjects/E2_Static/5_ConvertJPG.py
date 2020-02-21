from PIL import Image
import os

directory = "./Philippines/AllSubjects/E2_Static/data/imagery/"

for filename in os.listdir(directory):
    school_id = filename[0:6]
    im = Image.open(directory + filename).convert('RGB')
    new_name = "./Philippines/AllSubjects/E2_Static/data/jpg/" + school_id + '.jpg'
    im.save(new_name)
