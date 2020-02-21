# schoolCNN
Code and data to replicate "Learning about Learning with Deep Learning: Satellite Estimates of School Test Scores"

Code was written in R 3.5.1 and Python 3.6.8

## Description of folders

Each subject folder within Philippines has four subfolders:

 - E1_Landsat:
	 - Code to reproduce the Landsat CNN for each subject, including Landsat imagery preparation
 - E2_Static:
	 - Code to reproduce the Google Static CNN for each subject
 - E3_StreetView
	 - Code to reproduce the Google Street View CNN for each subject
 - Ensemble
	 - Code and data to generate the binary classification and absolute score prediction using the the results of each individual CNN

## Packages required

**R**

 - doParallel 
 - foreach
 -  jpeg
 -  raster
 -  rgdal
 -  rgeos
 -  sp

**Python**

 - Pandas
 - Numpy
 - torchvision 
 - imgaug 
 - torch 
 - matplotlib 
 - pickle 
 - joblib 
 - copy
 - time 
 - os 
 - sklearn

## Instructions for downloading Google Static and Street View imagery

Navigate to https://cloud.google.com/compute and set up an Google Compute Account. On your left drop down menu on the left-hand side of your dashboard, click on 'API's and Services. You will need to enable the Maps Static API and Street View API and generate API keys for each. Copy the generated API keys into the relevant Google API download files where it says 'API_KEY_HERE'




