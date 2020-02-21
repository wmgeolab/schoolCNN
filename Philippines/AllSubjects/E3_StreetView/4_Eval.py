from __future__ import print_function, division

from torchvision import datasets, models, transforms
from imgaug import parameters as iap
from imgaug import augmenters as iaa
from torch.optim import lr_scheduler
from torch.autograd import Variable
from torchsummary import summary
import matplotlib.pyplot as plt
import torch.optim as optim
import torch.nn as nn
from PIL import Image
import pandas as pd
import torchvision
import numpy as np
import pickle
import joblib
import torch
import time
import copy
import PIL
import os


class ImgAugTransform:
  def __init__(self):
    self.aug = iaa.Sequential([
        iaa.Scale((224, 224)),
        iaa.Sometimes(0.30, iaa.GaussianBlur(sigma=(0, 3.0))),
				iaa.Sometimes(0.25, iaa.Multiply((0.5, 1.5), per_channel=0.5)),
				iaa.Sometimes(0.20, iaa.Invert(0.25, per_channel=0.5)),
				iaa.Sometimes(0.25, iaa.ReplaceElementwise(
					iap.FromLowerResolution(iap.Binomial(0.1), size_px=8),
					iap.Normal(128, 0.4*128),
					per_channel=0.5)
										 ),
				iaa.Sometimes(0.30, iaa.AdditivePoissonNoise(40)),
        iaa.Fliplr(0.5),
        iaa.Affine(rotate=(-20, 20), mode='symmetric'),
        iaa.Sometimes(0.30,
                      iaa.OneOf([iaa.Dropout(p=(0, 0.1)),
                                 iaa.CoarseDropout(0.1, size_percent=0.5)])),
        iaa.AddToHueAndSaturation(value=(-10, 10), per_channel=True)
    ])
      
  def __call__(self, img):
    img = np.array(img)
    return self.aug.augment_image(img)

	
model_ft = models.resnext101_32x8d(pretrained = True)
optimizer_ft = optim.SGD(model_ft.parameters(), lr=0.001, momentum=0.9)
num_ftrs = model_ft.fc.in_features
model_ft.fc = nn.Linear(num_ftrs, 2)

checkpoint = torch.load("./Philippines/AllSubjects/E3_StreetView/models/Static_50epoch.torch")
model_ft.load_state_dict(checkpoint['model_state_dict'])

directory = "./Philippines/AllSubjects/E3_StreetView/data/imagery/"
transform = transforms.Compose([
	ImgAugTransform(),
	transforms.ToTensor(),
	transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])


def EvalModel(model, directory, transforms):
	model = model.cuda()
	df = pd.DataFrame()
	cpass, cfail, ids, h = [], [], [], []
	count = 0
	for filename in os.listdir(directory):
		count += 1
		school_id = filename[0:6]
		ids.append(school_id)
		heading = filename[10:13]
		h.append(heading)
		to_open = directory + filename
		png = Image.open(to_open)
		img_t = transform(png)
		batch_t = torch.unsqueeze(img_t, 0).cuda()
		model_ft.eval()
		out = model_ft(batch_t)
		_, index = torch.max(out, 1)
		percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100
		#			print(percentage)
		cfail.append(percentage[0].tolist())
		cpass.append(percentage[1].tolist())
		print("Predicted " + str(count) + " out of " + str(len(os.listdir(directory))) + " images." )
	df['school_id'] = ids
	df['heading'] = h
	df['prob_fail'] = cfail
	df['prob_pass'] = cpass
	return df



static_preds = EvalModel(model_ft, directory, transform)
static_preds.to_csv("./Philippines/AllSubjects/Ensemble/data/StreetViewPreds_GPU.csv")


