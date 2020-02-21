import pandas as pd
from sklearn.preprocessing import LabelEncoder

dta = pd.read_csv("./Philippines/Subject1_English/Ensemble1_English_LandsatResNeXt101/data/y1314_English.csv")
dta = dta.drop(['english_mean', 'latitude', 'longitude'], axis = 1)
dta.head()

sv = pd.read_csv("./Philippines/AllSubjects/Ensemble/data/StreetViewPreds_GPU.csv")
sv.head()

# Split along headings
h230 = sv[sv['heading'] == 230.0]
h50 = sv[sv['heading'] == 50.0]
h140 = sv[sv['heading'] == 140.0]
h330 = sv[sv['heading'] == 330.0]

h230 = h230[['school_id', 'prob_fail']]
h50 = h50[['school_id', 'prob_fail']]
h140 = h140[['school_id', 'prob_fail']]
h330 = h330[['school_id', 'prob_fail']]

h230.columns = ['school_id', 'h230_fail_pred']
h50.columns = ['school_id', 'h50_fail_pred']
h140.columns = ['school_id', 'h140_fail_pred']
h330.columns = ['school_id', 'h330_fail_pred']


# heading 230
h230['class_pred'] = 9
h230['class_pred'][h230['h230_fail_pred'] >= 50] = 1
h230['class_pred'][h230['h230_fail_pred'] < 50] = 0
h230 = pd.merge(h230, dta, on = 'school_id')

h230['correct'] = 0
h230["correct"][(h230['intervention'] == 0) & (h230["class_pred"] == 0)] = 1
h230["correct"][(h230['intervention'] == 1) & (h230["class_pred"] == 1)] = 1

#h230['class_pred'].value_counts()
#h230['intervention'].value_counts()
h230['correct'].value_counts()



# heading 50
h50['class_pred'] = 9
h50['class_pred'][h50['h50_fail_pred'] >= 50] = 1
h50['class_pred'][h50['h50_fail_pred'] < 50] = 0
h50 = pd.merge(h50, dta, on = 'school_id')

h50['correct'] = 0
h50["correct"][(h50['intervention'] == 0) & (h50["class_pred"] == 0)] = 1
h50["correct"][(h50['intervention'] == 1) & (h50["class_pred"] == 1)] = 1

#h50['class_pred'].value_counts()
#h50['intervention'].value_counts()
h50['correct'].value_counts()



# heading 140
h140['class_pred'] = 9
h140['class_pred'][h140['h140_fail_pred'] >= 50] = 1
h140['class_pred'][h140['h140_fail_pred'] < 50] = 0
h140 = pd.merge(h140, dta, on = 'school_id')

h140['correct'] = 0
h140["correct"][(h140['intervention'] == 0) & (h140["class_pred"] == 0)] = 1
h140["correct"][(h140['intervention'] == 1) & (h140["class_pred"] == 1)] = 1

#h140['class_pred'].value_counts()
#h140['intervention'].value_counts()
h140['correct'].value_counts()



# heading 330
h330['class_pred'] = 9
h330['class_pred'][h330['h330_fail_pred'] >= 50] = 1
h330['class_pred'][h330['h330_fail_pred'] < 50] = 0
h330 = pd.merge(h330, dta, on = 'school_id')

h330['correct'] = 0
h330["correct"][(h330['intervention'] == 0) & (h330["class_pred"] == 0)] = 1
h330["correct"][(h330['intervention'] == 1) & (h330["class_pred"] == 1)] = 1

#h330['class_pred'].value_counts()
#h330['intervention'].value_counts()
h330['correct'].value_counts()


h230 = h230.drop(['h230_fail_pred'], axis = 1)
h50 = h50.drop(['h50_fail_pred'], axis = 1)
h140 = h140.drop(['h140_fail_pred'], axis = 1)
h330 = h330.drop(['h330_fail_pred'], axis = 1)



comb = h230.append(h50)
comb = comb.append(h140)
comb = comb.append(h330)

comb['correct'].value_counts()



