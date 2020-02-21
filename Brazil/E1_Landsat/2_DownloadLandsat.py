import pandas as pd
#import geopandas as gpd
import os, shutil
from glob import glob
import requests
from bs4 import BeautifulSoup

prs = pd.read_csv("./Brazil/E1_Landsat/data/PRs.csv")
prs.head()

paths = prs['PATH'].tolist()
rows = prs['ROW'].tolist()

s3_scenes = pd.read_csv('http://landsat-pds.s3.amazonaws.com/c1/L8/scene_list.gz', compression='gzip')

# Empty list to add the images
bulk_list = []

# Iterate through paths and rows
for path, row in zip(paths, rows):

    print('Path:',path, 'Row:', row)

    # Filter the Landsat Amazon S3 table for images matching path, row, cloudcover and processing state.
    scenes = s3_scenes[(s3_scenes.path == path) & (s3_scenes.row == row) & 
                       (s3_scenes.cloudCover > 0) & (s3_scenes.cloudCover <= 100) & 
                       (~s3_scenes.productId.str.contains('_T2')) &
                       (~s3_scenes.productId.str.contains('_RT'))]
    print(' Found {} images\n'.format(len(scenes)))

    bulk_list.append(scenes)
        

        
bulk_frame = pd.concat(bulk_list)
bulk_frame2 = bulk_frame[bulk_frame['acquisitionDate'].str.contains('2015')]
bulk_frame2 = bulk_frame2.sort_values(by = ['productId', 'cloudCover'])
bulk_frame2['month'] = bulk_frame2['acquisitionDate'].str.split("-").str.get(1)
bulk_frame2 = bulk_frame2[bulk_frame2['month'] != '01']
bulk_frame2 = bulk_frame2.sort_values(by = ['productId', 'cloudCover'])
bulk_frame2['path'] = bulk_frame2['path'].astype(str)
bulk_frame2['row'] = bulk_frame2['row'].astype(str)
bulk_frame2['pr'] = bulk_frame2['path'] + bulk_frame2['row']
bulk_frame2['pr'] = bulk_frame2['path'] + bulk_frame2['row']
bulk_frame2 = bulk_frame2.drop_duplicates(subset = 'pr', keep = 'first')
bulk_frame2.head()
bulk_frame2.shape

	
	
# Download the relevant Landsat data
for i, row in bulk_frame2.iterrows():

    # Print some the product ID
    print('\n', 'EntityId:', row.productId, '\n')
    print(' Checking content: ', '\n')

    response = requests.get(row.download_url)

    if response.status_code == 200:

        html = BeautifulSoup(response.content, 'html.parser')

        entity_dir = os.path.join("./Brazil/E1_Landsat/data/Landsat/", row.productId)
        os.makedirs(entity_dir, exist_ok=True)

        for li in html.find_all('li'):

            file = li.find_next('a').get('href')

            print('  Downloading: {}'.format(file))

            response = requests.get(row.download_url.replace('index.html', file), stream=True)

            with open(os.path.join(entity_dir, file), 'wb') as output:
                shutil.copyfileobj(response.raw, output)
            del response