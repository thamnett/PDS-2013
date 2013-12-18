# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

%matplotlib inline
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import operator
from operator import itemgetter
from pprint import pprint
from pandas import *
from datetime import datetime
from sklearn.linear_model import SGDClassifier
from sklearn.datasets.samples_generator import make_blobs
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn import svm
from sklearn import cross_validation
from sklearn import metrics
from sklearn.neighbors import KNeighborsRegressor

#!curl -s 'people.stern.nyu.edu/ja1517/pdsfall2012/ad.json' > assess2.json

data = []
with open('assess2.json', 'r') as f:
    for line in f:
        data.append(json.loads(line))
        
f.close()

#pprint(data[:1])

num_bad = 0

clean_data = []

#!grep -v -w "?" assess2.json > clean_asess2.json

#!wc clean_asess2.json

for element in data:
    x = 0
    for val in element:
        if val == "?":
            x += 1
        else:
            pass
    if x >= 1:
        num_bad += 1
    else:
        clean_data.append(element)

print "The number of records with ? is: %i" % num_bad
#The number of records with ? is: 920

ads_data_lst = []
ads_target_lst = []

for element in clean_data:
    length = len(element)
    for i in range(length-1):
        element[i] = float(element[i])
    if element[length-1] == "ad.":
        element[length-1] = 1.0
    elif element[length-1] == "nonad.":
        element[length-1] = 0.0
    else:
        pass
    ads_data_lst.append(element[:length-1])
    ads_target_lst.append(element[length-1])

# numpy arrays
ads_data = np.array(ads_data_lst)
ads_target = np.array(ads_target_lst)

# create a logistic regression model
model2 = LogisticRegression()

# "train" the model, fit it to the vectors of the training data and their respective labels.
logfit = model2.fit(ads_data, ads_target)

neighmodel = KNeighborsRegressor(n_neighbors=5)
neighfit = neighmodel.fit(ads_data, ads_target)

print "The accuracy of the logistic regression model when applied to the training data is: %f" \
% logfit.score(ads_data, ads_target)
#The accuracy of the logistic regression model when applied to the training data is: 0.981772


svcmodel = svm.SVC()

svcfit = svcmodel.fit(ads_data, ads_target)

print "The accuracy of the decision tree model when applied to the training data is: %f" \
% svcfit.score(ads_data, ads_target)
#The accuracy of the decision tree model when applied to the training data is: 0.931751

folds = 19

vals = []

for i in range(1,folds+1):
    vals.append(float(i)/float(folds+1))

logscore = []
svcscore = []
neighscore = []
logdict = {}
svcdict = {}
neighdict = {}

for i in range(1,folds+1):
    x_train, x_test, y_train, y_test \
    = cross_validation.train_test_split(ads_data, ads_target, test_size=.05*i, random_state=0)    
    logscore.append(model2.fit(x_train,y_train).score(x_test,y_test))
    logdict[vals[i-1]] = model2.fit(x_train,y_train).score(x_test,y_test)
    svcscore.append(svcmodel.fit(x_train,y_train).score(x_test,y_test))
    svcdict[vals[i-1]] = svcmodel.fit(x_train,y_train).score(x_test,y_test)
    neighscore.append(neighmodel.fit(x_train,y_train).score(x_test,y_test))
    neighdict[vals[i-1]] = neighmodel.fit(x_train,y_train).score(x_test,y_test)

    
#print scores
print "Log Scores"
pprint(logdict)
print "SVC Scores"
pprint(svcdict)
print "Neighbors Scores"
pprint(neighdict)

#Log Scores
#{0.05: 0.9576271186440678,
# 0.1: 0.96610169491525422,
# 0.15: 0.97175141242937857,
# 0.2: 0.97033898305084743,
# 0.25: 0.97288135593220337,
# 0.3: 0.9731638418079096,
# 0.35: 0.97215496368038745,
# 0.4: 0.96398305084745761,
# 0.45: 0.967984934086629,
# 0.5: 0.96355932203389827,
# 0.55: 0.95993836671802768,
# 0.6: 0.9597457627118644,
# 0.65: 0.95893089960886568,
# 0.7: 0.95278450363196121,
# 0.75: 0.94971751412429384,
# 0.8: 0.95286016949152541,
# 0.85: 0.9456630109670987,
# 0.9: 0.94538606403013181,
# 0.95: 0.92729705619982161}

#SVC Scores
#{0.05: 0.94067796610169496,
# 0.1: 0.94067796610169496,
# 0.15: 0.93220338983050843,
# 0.2: 0.93220338983050843,
# 0.25: 0.93559322033898307,
# 0.3: 0.93361581920903958,
# 0.35: 0.93341404358353508,
# 0.4: 0.92902542372881358,
# 0.45: 0.92937853107344637,
# 0.5: 0.92881355932203391,
# 0.55: 0.92681047765793534,
# 0.6: 0.9307909604519774,
# 0.65: 0.92242503259452413,
# 0.7: 0.91949152542372881,
# 0.75: 0.91807909604519777,
# 0.8: 0.92002118644067798,
# 0.85: 0.91924227318045859,
# 0.9: 0.92184557438794723,
# 0.95: 0.91971454058876001}

#Neighbors Scores
#{0.05: 0.70861224489795882,
# 0.1: 0.6806294256490939,
# 0.15: 0.66364670458347264,
# 0.2: 0.66697777777777945,
# 0.25: 0.68427200289750045,
# 0.3: 0.69188888888889166,
# 0.35: 0.68621954414461583,
# 0.4: 0.64051009244799006,
# 0.45: 0.64753960857409232,
# 0.5: 0.63657292185167325,
# 0.55: 0.61767337577873938,
# 0.6: 0.58863583410998199,
# 0.65: 0.57147671201399586,
# 0.7: 0.55483381924196906,
# 0.75: 0.54766966252794225,
# 0.8: 0.51659378596088534,
# 0.85: 0.4756558236010352,
# 0.9: 0.42279592370004948,
# 0.95: 0.31012047026948264}

plt.scatter(vals, logscore, s=50, label='Log')
plt.scatter(vals, svcscore, s=50, color='g', label='SVC')
plt.scatter(vals, neighscore, s=50, color='c', label='Neigh')
plt.legend(loc=3)
plt.show

# <codecell>


# <codecell>


