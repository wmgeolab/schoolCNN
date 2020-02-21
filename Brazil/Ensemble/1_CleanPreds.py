import pandas as pd
from sklearn.preprocessing import LabelEncoder

dta = pd.read_csv("./Brazil/E1_Landsat/data/y15_Brazil.csv")
dta = dta.drop(['passing', 'latitude', 'longitude'], axis = 1)
dta.head()

# Landsat
landsat_pass = pd.read_csv("./Brazil/Ensemble/data/LandsatPassPreds.csv")
landsat_pass = landsat_pass.drop(['Unnamed: 0'], axis = 1)
landsat_pass.head()
landsat_pass.shape

landsat_fail = pd.read_csv("./Brazil/Ensemble/data/LandsatFailPreds.csv")
landsat_fail = landsat_fail.drop(['Unnamed: 0'], axis = 1)
landsat_fail.head()
landsat_fail.shape

landsat_preds = landsat_pass.append(landsat_fail)
landsat_preds['school_id'] = landsat_preds['school_id'].str[:-3]
landsat_preds['school_id'] = landsat_preds['school_id'].astype(int)
landsat_preds['landsat_class_pred'] = 9
landsat_preds['landsat_class_pred'][landsat_preds['prob_pass'] >= 50] = 0
landsat_preds['landsat_class_pred'][landsat_preds['prob_pass'] < 50] = 1
landsat_preds = pd.merge(landsat_preds, dta, on = 'school_id')

landsat_preds['correct'] = 0
landsat_preds["correct"][(landsat_preds['intervention'] == 0) & (landsat_preds["landsat_class_pred"] == 0)] = 1
landsat_preds["correct"][(landsat_preds['intervention'] == 1) & (landsat_preds["landsat_class_pred"] == 1)] = 1

landsat_preds['landsat_class_pred'].value_counts()
landsat_preds['intervention'].value_counts()
landsat_preds['correct'].value_counts()

print(sum(landsat_preds['correct']) / len(landsat_preds))



# Static
static = pd.read_csv("./Brazil/Ensemble/data/BrazilPreds.csv")
static = static.drop(['Unnamed: 0'], axis = 1)
#static['school_id'] = static['school_id'].str.replace(".pn", "").str.replace(".", "").astype(int)
static.head()

static['static_class_pred'] = 9
static['static_class_pred'][static['prob_pass'] >= 50] = 0
static['static_class_pred'][static['prob_pass'] < 50] = 1
static = pd.merge(static, dta, on = 'school_id')

static['correct'] = 0
static["correct"][(static['intervention'] == 0) & (static["static_class_pred"] == 0)] = 1
static["correct"][(static['intervention'] == 1) & (static["static_class_pred"] == 1)] = 1

static['static_class_pred'].value_counts()
static['intervention'].value_counts()
static['correct'].value_counts()

print(sum(static['correct']) / len(static))


sv = pd.read_csv("./Brazil/Ensemble/data/StreetViewPreds.csv")
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

#h230.columns = ['school_id', 'h230_pass_pred']
#h50.columns = ['school_id', 'h50_pass_pred']
#h140.columns = ['school_id', 'h140_pass_pred']
#h330.columns = ['school_id', 'h330_pass_pred']

#sv_preds = sv[['school_id','label']]
#sv_preds = sv_preds.drop_duplicates(subset = 'school_id')

merged = pd.merge(h50, h140, on = 'school_id')
merged = pd.merge(merged, h230, on = 'school_id')
merged = pd.merge(merged, h330, on = 'school_id')
#merged = pd.merge(merged, preds, on = 'school_id')
merged.head()
merged.shape



# Prep for Ensemble
landsat_preds = landsat_preds.drop(['correct', 'prob_pass', 'landsat_class_pred', 'intervention'], axis = 1)
static = static.drop(['correct', 'prob_pass', 'static_class_pred'], axis = 1)

landsat_preds.columns = ['school_id', 'landsat_prob_fail']
static.columns = ['school_id', 'static_prob_fail', 'intervention']


comb = pd.merge(landsat_preds, static, on = 'school_id')
comb = pd.merge(comb, merged, on = 'school_id')

comb = comb.fillna(-1)



comb.shape



comb.to_csv("./Brazil/Ensemble/data/EnsemblePreds.csv", index = False)