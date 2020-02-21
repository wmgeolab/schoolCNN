import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as cm
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn import tree
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn import linear_model
from sklearn.linear_model import Ridge
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import BaggingRegressor


# Read in and split data into training and validation sets 
df = pd.read_csv("./Philippines/Subject1_English/Ensemble1_English_LandsatResNeXt101/data/y1314_English.csv")
df = df.drop(['intervention', 'latitude', 'longitude'], axis = 1)
#df['english_mean'] = df['overall_mean'] / 5
df.head()

dta = pd.read_csv("./Philippines/Subject1_English/Ensemble/data/EnsemblePreds_GPU.csv")
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

y_train = train.pop("english_mean")
x_train = train

y_test = test.pop("english_mean")
x_test = test


svr_regression = SVR(kernel = 'linear', epsilon = 1.0)
svr_regressionFit = svr_regression.fit(x_train, y_train)

DT_regression = tree.DecisionTreeRegressor(random_state = 1693, max_depth = 3)
DT_regressionFit = DT_regression.fit(x_train, y_train)

RF_regression = RandomForestRegressor(n_estimators = 100, random_state = 1693)
RF_regressionFit = RF_regression.fit(x_train, y_train)
rf_MAD = mean_absolute_error(y_test, RF_regressionFit.predict(x_test))
print('Random Forest Tree MAD: ' + str(rf_MAD))

neigh = KNeighborsRegressor(n_neighbors=2)
neighFit = neigh.fit(x_train, y_train)

mlp = MLPRegressor()
mlpFit = mlp.fit(x_train, y_train)

regr = AdaBoostRegressor(random_state=0, n_estimators=100)
regrFit = regr.fit(x_train, y_train)

clfRidge = Ridge(alpha=1.0)
clfRidgeFit = clfRidge.fit(x_train, y_train)

clfBayesian = linear_model.BayesianRidge()
clfBayesianFit = clfBayesian.fit(x_train, y_train)

reg = linear_model.LassoLars(alpha=0.01)
regFit = reg.fit(x_train, y_train)

bag = BaggingRegressor()
bagFit = bag.fit(x_train, y_train)




DT_MAD = mean_absolute_error(y_test, DT_regressionFit.predict(x_test))
SVR_MAD = mean_absolute_error(y_test, svr_regressionFit.predict(x_test))
KNN_MAD = mean_absolute_error(y_test, neighFit.predict(x_test))
MLP_MAD = mean_absolute_error(y_test, mlpFit.predict(x_test))
regr_MAD = mean_absolute_error(y_test, mlpFit.predict(x_test))
clfRidge_MAD = mean_absolute_error(y_test, clfRidgeFit.predict(x_test))
clfBayesion_MAD = mean_absolute_error(y_test, clfBayesianFit.predict(x_test))
reg_MAD = mean_absolute_error(y_test, regFit.predict(x_test))
bag_MAD = mean_absolute_error(y_test, bagFit.predict(x_test))



print('Regression Tree MAD: ' + str(DT_MAD))
print('Support Vector Regression MAD ' + str(SVR_MAD))
print('KNN MAD ' + str(KNN_MAD))
print('MLP MAD ' + str(MLP_MAD))
print('AdaBoost MAD ' + str(regr_MAD))
print('CLF Ridge MAD ' + str(clfRidge_MAD))
print('CLF Bayesion MAD ' + str(clfBayesion_MAD))
print('Reg MAD ' + str(reg_MAD))
print('Bag MAD ' + str(bag_MAD))





to_pred = dta.drop(['english_mean'], axis = 1)
preds = RF_regressionFit.predict(to_pred)

dta = pd.read_csv("./Philippines/Subject1_English/Ensemble/data/EnsemblePreds.csv")
df = pd.read_csv("./Philippines/Subject1_English/Ensemble1_English_LandsatResNeXt101/data/y1314_English.csv")
dta = pd.merge(dta, df, on = 'school_id')

final_df = pd.DataFrame()
final_df['school_id'] = dta['school_id']
final_df['intervention'] = dta['intervention_x']
final_df['actual_mean'] = dta['english_mean']
final_df['predicted_mean'] = preds.tolist()
final_df['error'] = abs(final_df['actual_mean'] - final_df['predicted_mean'])

final_df['error'].mean()
final_df['error'].std()
final_df['actual_mean'].mean()
final_df['predicted_mean'].mean()
final_df['actual_mean'].std()
final_df['predicted_mean'].std()

final_df.to_csv("./Philippines/Subject1_English/Ensemble/data/PredictedAbsolute_English.csv")