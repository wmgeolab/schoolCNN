import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as cm
import numpy as np
from sklearn.model_selection import train_test_split

dta = pd.read_csv("./Philippines/Subject4_Science/Ensemble/data/EnsemblePreds_GPU.csv")
dta = dta.drop(['school_id'], axis = 1)
dta.head()

# Train Test split the data
msk = np.random.rand(len(dta)) < 0.8

train = dta[msk]
test = dta[~msk]

y_train = train.pop("intervention")
x_train = train

y_test = test.pop("intervention")
x_test = test


# Nearest Neighbors
from sklearn.neighbors import KNeighborsClassifier
NNeighbors = KNeighborsClassifier(n_neighbors=10).fit(x_train, y_train)
Z = NNeighbors.predict(x_test)
1 - (sum(abs(Z - y_test)) / len(y_test))


# MLP Classifier
from sklearn.neural_network import MLPClassifier
MLP = MLPClassifier(alpha=1, max_iter=1000, random_state=1693).fit(x_train, y_train)
Z = MLP.predict(x_test)
1 - (sum(abs(Z - y_test)) / len(y_test))


# Linear SVM
from sklearn.svm import SVC
linear_svm = SVC(probability=True).fit(x_train, y_train)
Z = linear_svm.predict(x_test)
1 - (sum(abs(Z - y_test)) / len(y_test))


# Radial SVM
from sklearn.svm import SVC
radial_svm = SVC(gamma=2, C=1, probability=True).fit(x_train, y_train)
Z = radial_svm.predict(x_test)
1 - (sum(abs(Z - y_test)) / len(y_test))


# Decision Tree
from sklearn.tree import DecisionTreeClassifier
dTree = DecisionTreeClassifier(random_state = 1693).fit(x_train, y_train)
Z = dTree.predict(x_test)
1 - (sum(abs(Z - y_test)) / len(y_test))


# Random Forest
from sklearn.ensemble import RandomForestClassifier
rForest = RandomForestClassifier(n_estimators = 1000, random_state=1693, max_depth=3).fit(x_train, y_train)
Z = rForest.predict(x_test)
1 - (sum(abs(Z - y_test)) / len(y_test))

