from urllib.request import urlopen
import pandas as pd
import urllib, os
import json

coords = pd.read_csv("./Brazil/data/BrazilCleaned.py")
coords.head()
coords.shape

    
def GetImage(lat, long, school_id, heading):
	base = "https://maps.googleapis.com/maps/api/streetview/metadata?location="
	lat = str(lat)
	long = str(long)
	url = base + lat + ',' + long + "&heading=" + str(heading) + "&key=API_KEY_HERE"
	file = "./Brazil/E3_StreetView/data/json/temp.json"
	urllib.request.urlretrieve(url, file)
	with open(file) as temp:
		data = json.load(temp)
		if data['status'] != 'ZERO_RESULTS':
			new_base = "https://maps.googleapis.com/maps/api/streetview?size=224x224&location="
			url = new_base + lat + ',' + long + "&heading=" + str(heading) + "&key=API_KEY_HERE"
			save_name = "./Brazil/E3_StreetView/data/imagery/" + str(school_id) + "_h" + str(heading) + ".png"
			urllib.request.urlretrieve(url, save_name)

  
count = 1

for index, row in coords.iterrows():
    msg = "File #" + str(count)
    print(msg)
    GetImage(row['latitude'], row['longitude'], row['school_id'], 330)
    count += 1


count = 1
for index, row in coords.iterrows():
    msg = "File #" + str(count)
    print(msg)
    GetImage(row['latitude'], row['longitude'], row['school_id'], 50)
    count += 1

		
count = 1	
for index, row in coords.iterrows():
    msg = "File #" + str(count)
    print(msg)
    GetImage(row['latitude'], row['longitude'], row['school_id'], 140)
    count += 1

		
count = 1
for index, row in coords.iterrows():
    msg = "File #" + str(count)
    print(msg)
    GetImage(row['latitude'], row['longitude'], row['school_id'], 230)
    count += 1
