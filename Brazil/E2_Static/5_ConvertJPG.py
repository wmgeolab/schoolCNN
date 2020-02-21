from PIL import Image
import os

directory = "./Brazil/E2_Static/data/imagery/"

for filename in os.listdir(directory):
    school_id = filename[0:11]
    im = Image.open(directory + filename).convert('RGB')
    new_name = "./Brazil/E2_Static/data/jpg/" + school_id + '.jpg'
    im.save(new_name)
