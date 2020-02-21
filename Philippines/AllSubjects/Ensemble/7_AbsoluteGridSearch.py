from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
import matplotlib.colors as cm
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.svm import SVR
from sklearn import tree
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor





# Read in and split data into training and validation sets 
df = pd.read_csv("./Philippines/AllSubjects/Ensemble1_LandsatResNeXt101/data/y1314_AllSubjects.csv")
df = df.drop(['intervention', 'latitude', 'longitude'], axis = 1)
df['overall_mean'] = df['overall_mean'] / 5

dta = pd.read_csv("./Philippines/AllSubjects/Ensemble/data/EnsemblePreds_GPU.csv")
dta = pd.merge(dta, df, on = 'school_id')
dta = dta.drop(['intervention'], axis = 1)
dta.shape
dta.head()

dta = dta.drop(['school_id'], axis = 1)
dta.head()

# Train Test split the data
msk = np.random.rand(len(dta)) < 0.8

train = dta[msk]
test = dta[~msk]

y_train = train.pop("overall_mean")
x_train = train

y_test = test.pop("overall_mean")
x_test = test





# Random Forest Grid Search
RF_regression = RandomForestRegressor()
RF_regressionFit = RF_regression.fit(x_train, y_train)
rf_MAD = mean_absolute_error(y_test, RF_regressionFit.predict(x_test))
print('Random Forest Tree MAD: ' + str(rf_MAD))


params = [{'n_estimators':[5, 7, 9, 10, 20, 250, 500, 750, 800, 900, 1000, 1100, 1200, 1250, 1500, 2980, 2990],
           'max_depth':[None, 1,2,3,4,5,6,7,8,9,10],
					 'min_samples_split':[2,3,4,5],
					 'min_samples_leaf':[1,2,3,4,5],
					 'max_features':['auto', 'sqrt', 'log2']}]

gSearch = GridSearchCV(estimator = RF_regressionFit, 
                       param_grid = params,
                       scoring = 'neg_mean_absolute_error',
                       cv=10)

gSearch_results = gSearch.fit(x_train, y_train)
gSearch_results.best_params_
gSearch_results.best_score_





# SVR Grid Search
svr_regression = SVR(kernel = 'linear')
svr_regressionFit = svr_regression.fit(x_train, y_train)
SVR_MAD = mean_absolute_error(y_test, svr_regressionFit.predict(x_test))
print('Support Vector Regression MAD ' + str(SVR_MAD))


params = [{'kernel':['linear', 'poly', 'rbf', 'sigmoid', 'precomputed'],
           'degree':[1,2,3,4,5], 
					 'gamma':['scale', 'auto'],
           'epsilon':[.1, .15, .2, .25, .3, .4, .5],
					 'shrinking':[True, False]}]

gSearch = GridSearchCV(estimator = svr_regressionFit, 
                       param_grid = params,
                       scoring = 'neg_mean_absolute_error',
                       cv=10)

gSearch_results = gSearch.fit(x_train, y_train)
gSearch_results.best_params_
gSearch_results.best_score_





# Nearest Neighbors Grid Search
neigh = KNeighborsRegressor()
neighFit = neigh.fit(x_train, y_train)
KNN_MAD = mean_absolute_error(y_test, neighFit.predict(x_test))
print('KNN MAD ' + str(KNN_MAD))


params = [{'n_neighbors':[1,2,3,4,5,6,7,8,9,10],
           'weights':['uniform', 'distance'], 
					 'algorithm':['auto', 'ball_tree', 'kd_tree', 'brute'],
           'leaf_size':[10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40],
					 'p':[1,2]}]

gSearch = GridSearchCV(estimator = neighFit, 
                       param_grid = params,
                       scoring = 'neg_mean_absolute_error',
                       cv=10)

gSearch_results = gSearch.fit(x_train, y_train)
gSearch_results.best_params_
gSearch_results.best_score_





# Decision Tree Grid Search
DT_regression = tree.DecisionTreeRegressor()
DT_regressionFit = DT_regression.fit(x_train, y_train)
DT_MAD = mean_absolute_error(y_test, DT_regressionFit.predict(x_test))
print('Decision Tree MAD: ' + str(DT_MAD))

params = [{'criterion':['mse', 'friedman_mse', 'mae'],
					 'splitter':['best', 'random'],
           'max_depth':[None,1,2,3,4,5,6,7,8,9,10],
           'min_samples_split':[2,3,4,5],
					 'min_samples_leaf':[1,2,3,4,5],
					 'max_features':['auto', 'sqrt', 'log2']}]

gSearch = GridSearchCV(estimator = DT_regressionFit, 
                       param_grid = params,
                       scoring = 'neg_mean_absolute_error',
                       cv=10)

gSearch_results = gSearch.fit(x_train, y_train)
gSearch_results.best_params_
gSearch_results.best_score_





# MLP Grid Search
mlp = MLPRegressor()
mlpFit = mlp.fit(x_train, y_train)
MLP_MAD = mean_absolute_error(y_test, mlpFit.predict(x_test))
print('MLP MAD ' + str(MLP_MAD))


params = [{'activation':['identity', 'logistic', 'tanh', 'relu'],
					 'solver':['lbfgs', 'sgd', 'adam'],
           'alpha':[0.0001, 0.0002, 0.0003, 0.0004, 0.0005],
           'learning_rate':['constant', 'invscaling', 'adaptive'],
					 'momentum':[.5, .6, .7, .8, .9]}]

gSearch = GridSearchCV(estimator = mlpFit, 
                       param_grid = params,
                       scoring = 'neg_mean_absolute_error',
                       cv=10)

gSearch_results = gSearch.fit(x_train, y_train)
gSearch_results.best_params_
gSearch_results.best_score_




