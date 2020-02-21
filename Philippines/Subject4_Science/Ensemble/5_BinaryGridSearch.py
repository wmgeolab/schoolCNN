from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
import matplotlib.colors as cm
import seaborn as sns
import pandas as pd
import numpy as np


dta = pd.read_csv("./Philippines/Subject4_Science/Ensemble/data/EnsemblePreds_GPU.csv")
#dta = dta.drop(['school_id'], axis = 1)
dta.head()

# Train Test split the data
msk = np.random.rand(len(dta)) < 0.8

train = dta[msk]
test = dta[~msk]

y_train = train.pop("intervention")
x_train = train

y_test = test.pop("intervention")
x_test = test


# Random Forest Grid Search
rForest = RandomForestClassifier().fit(x_train, y_train)
Z = rForest.predict(x_test)
1 - (sum(abs(Z - y_test)) / len(y_test))

params = [{'n_estimators':[10, 20, 250, 500, 750, 800, 900, 1000, 1100, 1200, 1250, 1500, 2980, 2990],
           'max_depth':[1,2,3,4,5,6,7,8,9,10]
#					 'criterion':['gini', 'entropy']
#					 'min_samples_split':[2,3,4,5],
#           'min_samples_leaf':[1,2,3,4,5],
#					 'max_features': ['auto', 'sqrt', 'log2']
					}]

gSearch = GridSearchCV(estimator = rForest, 
                       param_grid = params,
                       scoring = 'accuracy',
                       cv=10)

gSearch_results = gSearch.fit(x_train, y_train)
gSearch_results.best_params_
gSearch_results.best_score_
gSearch_results.cv_results_



# Nearest Neighbors Grid Search
NNeighbors = KNeighborsClassifier().fit(x_train, y_train)
Z = NNeighbors.predict(x_test)
1 - (sum(abs(Z - y_test)) / len(y_test))

params = [{'n_neighbors': [1,2,3,4,5,6,7,8,9,10],
           'weights': ['uniform', 'distance'], 
           'leaf_size': [10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40],
					 'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
					 'p':[1,2]}]

gSearch = GridSearchCV(estimator = NNeighbors, 
                       param_grid = params,
                       scoring = 'accuracy',
                       cv=10)

gSearch_results = gSearch.fit(x_train, y_train)
gSearch_results.best_params_
gSearch_results.best_score_
gSearch_results.cv_results_



# Decision Tree Grid Search
dTree = DecisionTreeClassifier().fit(x_train, y_train)
Z = dTree.predict(x_test)
1 - (sum(abs(Z - y_test)) / len(y_test))

params = [{'criterion':['gini', 'entropy'],
					 'splitter':['best', 'random'],
           'max_depth':[1,2,3,4,5,6,7,8,9,10],
#           'min_samples_split':[2,3,4,5],
#           'min_samples_leaf':[1,2,3,4,5],
					 'max_features': ['auto', 'sqrt', 'log2']}]

gSearch = GridSearchCV(estimator = dTree, 
                       param_grid = params,
                       scoring = 'accuracy',
                       cv=10)

gSearch_results = gSearch.fit(x_train, y_train)
gSearch_results.best_params_
gSearch_results.best_score_
gSearch_results.cv_results_

