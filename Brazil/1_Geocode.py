import pandas as pd
import urllib, os
import os
import urllib
import json

geo = pd.read_csv("./Brazil/data/ToGeocode.csv", encoding= 'unicode_escape')
geo['municipality'] = geo['municipality'].str.replace("©", '').replace("£", '').replace("Ã", 'a')
geo['municipality'] = geo['municipality'].str.replace("¢", '').replace("³", '').replace("§", '')
geo['municipality'] = geo['municipality'].str.replace("ª", '').replace("º", '').replace("¡", '')
geo.head()
geo.shape



def GetGoogleStatic(name, state, munic, school_id):
	try:
		base = "https://maps.googleapis.com/maps/api/geocode/json?address="   
		url = base + name.replace(" ", "+") + '&components=locality:' + state.replace(" ", "+") +'|sublocality:' + munic.replace(" ", "+") + '|country:BR&type=school|university|primary_school|secondary_school&country=BR&key=API_KEY_HERE'
		file = "./Brazil/data/jsons/" + str(school_id) + ".json"
		urllib.request.urlretrieve(url, file)
	except:
		print("Couldn't save file: " + str(school_id))


count = 0

for index, row in geo.iterrows():
	msg = "File #" + str(count)
	print(msg)
	GetGoogleStatic(row['school_name'], row['state'], row['municipality'], row['school_id'])
	count += 1

	
	
	