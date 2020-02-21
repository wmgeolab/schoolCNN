import pandas as pd
import json
import csv


directory = "./Brazil/data/jsons/"
school_ids, lats, longs, types = [], [], [], []

# Convert the JSONs into a dataframe
for file in os.listdir(directory):
	school_ids.append(file)
	fname = directory + file
	with open(fname) as file:
		data = json.load(file)
		if data['status'] != 'ZERO_RESULTS':
			lat = data['results'][0]['geometry']['location']['lat']
			long = data['results'][0]['geometry']['location']['lng']
			ptype = data['results'][0]['types']
			lats.append(lat)
			longs.append(long)
			types.append(ptype)
		else:
			lats.append(0)
			longs.append(0)
			types.append(-999)

df = pd.DataFrame()
df['school_id'] = school_ids
df['school_id'] = df['school_id'].str.strip(".json")
df['latitude'], df['longitude'], df['type'] = lats, longs, types


# Remove and points that did not return results
df = df[df['type'] != -999]


# Remove any points that are not categorized as relating to education
drop = []
for k,v in df.iterrows():
	if ('school' not in v.type) and ('university' not in v.type) and ('primary_school' not in v.type) and ('secondary_school' not in v.type):
		drop.append(v.school_id)
df = df[~df['school_id'].isin(drop)]


print("Number of JSONS: ", len(os.listdir("./Brazil/data/jsons/")))
print("Number of confirmed schools: ", len(df))


df.to_csv("./Brazil/data/SchoolCoords_Brazil.csv")