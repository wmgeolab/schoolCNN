import pandas as pd
import urllib, os

coords = pd.read_csv("./clean/AllSubjects/E2_Static/data/y1314_AllSubjects.csv")

coords = coords[0:2]
coords.head()
coords.shape

    
def GetGoogleStatic(lat, long, school_id, intervention):
    base = "https://maps.googleapis.com/maps/api/staticmap?center="
    lat = str(lat)
    long = str(long)
    url = base + lat + ',' + long + "&zoom=18&size=224x224&maptype=satellite&key=INSERT_API_KEY_HERE"
    file = "./clean/AllSubjects/E2_Static/imagery/" + str(school_id) + ".png"
    print(url)
    urllib.request.urlretrieve(url, file)
  
  
count = 1

for index, row in coords.iterrows():
    msg = "File #" + str(count)
    print(msg)
    GetGoogleStatic(row['latitude'], row['longitude'], row['school_id'], row['intervention'])
    count += 1

		
		
