import pandas as pd

coords = pd.read_csv("./Brazil/data/SchoolCoords_Brazil.csv")
df = pd.read_csv("./Brazil/data/ToGeocode.csv")

comb = pd.merge(coords, df, on = 'school_id')
comb.head()

comb = comb[['school_id', 'latitude', 'longitude',
						'state', 'passing']]

comb = comb[comb['state'].isin(['Sao Paulo', 'Minas Gerais',
															 'Rio de Janeiro', 'Parana'])]

comb.to_csv("./Brazil/data/BrazilCleaned.py")