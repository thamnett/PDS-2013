# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import matplotlib.pyplot as plt
import numpy as np
import json
import operator
from operator import itemgetter
from pprint import pprint

#File is JSON structure
#Use head assess1_data.json to get fields
#Fields are: RFA_2F, RFA_2A, TARGET_B, LASTGIFT, AVGGIFT, PEPSTRFL, LASTDATE,
#WEALTH_INDEX, INCOME, FISTDATE, NAME
#Use wc assess1_data.json to get number of customers (lines)
#Number of customers is 35275

#Load data into python

data = []
with open('assess1_data.json', 'r') as f:
    for line in f:
        data.append(json.loads(line))
        
f.close()

name_count = {}

#Create dict with count of name instances

for element in data:
    if element.get("NAME") in name_count:
        name_count[element.get("NAME")] += 1
    else:
        name_count[element.get("NAME")] = 1

#List duplicate names
        
for key in name_count:
    if name_count[key] >=2:
        print "%s has multiple entries." % key
    else:
        pass

#Output is one name: Sneha K. O'Hooper
#Clean up data for -9999 or '-9999' values

clean_data = []
num_bad = 0

for element in data:
    x = 0
    for val in element.itervalues():
        if val == -9999:
            x += 1
        elif val == "-9999":
            x += 1
        else:
            pass
    if x >= 1:
        num_bad += 1
    else:
        clean_data.append(element)

print len(clean_data)
print "%i rows have -9999 as value in the row." % num_bad

#2 rows have value -9999
#Create dicts for recency, fequency, and wealth, and counts of each

recency_dict= {}
freq_dict = {}
wealth_dict = {}

for element in clean_data:
    if element.get("RFA_2F") in recency_dict:
        recency_dict[element.get("RFA_2F")] += 1
    else:
        recency_dict[element.get("RFA_2F")] = 1
    if element.get("RFA_2A") in freq_dict:
        freq_dict[element.get("RFA_2A")] += 1
    else:
        freq_dict[element.get("RFA_2A")] = 1
    if element.get("WEALTH_INDEX") in wealth_dict:
        wealth_dict[element.get("WEALTH_INDEX")] += 1
    else:
        wealth_dict[element.get("WEALTH_INDEX")] = 1

print "The values and frequency of RFA_2F are:"
print recency_dict
print "The values and frequency of RFA_2A are:"
print freq_dict
print "Wealth index range is from %f to %f" % (min(wealth_dict.keys()), max(wealth_dict.keys()))

#Values and frequency of RFA_2F are:
#{1: 12530, 2: 8134, 3: 7367, 4: 7241}
#Values and frequency of RFA_2A are:
#{u'E': 12884, u'D': 5074, u'G': 5125, u'F': 12189}
#WEALTH_INDEX range from 0.01 to 99.85
#Appears to be a two decimal number on scale from 0 to 100

num_respond = 0

for element in clean_data:
    num_respond += element.get("TARGET_B")

print "The number of responses is: %i" % num_respond
print "The proportion of responses is: %f" % (num_respond / float(len(clean_data)))

#Number of responses is 2226, or 6.311% of total

resp_wealth = []
noresp_wealth = []

for element in clean_data:
    if element.get("TARGET_B") == 0:
        noresp_wealth.append(element.get("WEALTH_INDEX"))
    elif element.get("TARGET_B") == 1:
        resp_wealth.append(element.get("WEALTH_INDEX"))
    else:
        pass

bin_lst = [0,10,20,30,40,50,60,70,80,90,100]

plt.hist(resp_wealth, bins=bin_lst, alpha=0.5, label='Respond')
plt.hist(noresp_wealth, bins=bin_lst, alpha=0.5, label='No Respond')
plt.legend()
plt.show()

plt.hist(resp_wealth, bins=bin_lst, normed=True, alpha=0.5, label='Respond')
plt.hist(noresp_wealth, bins=bin_lst, normed=True, alpha=0.5, label='No Respond')
plt.legend()
plt.show()

#Non-responders are more highly concentrated towards the lower end of the
#wealth index than responders
#On a count basis, non-responders exceed responders in the bottom four (of ten)
#tranches, while responders exceed in the top six tranches
#On a percentage basis, non-reponders exceed respondere in the lowest tranch (of ten)
#of the wealth index, but are lower proportion in every other tranch

clean_data = sorted(clean_data,key=itemgetter("NAME"))

alph_numbered = []
num = 1

for element in clean_data:
    element["ALPHA"] = num
    num += 1
    alph_numbered.append(element)

pprint(alph_numbered[:10])
pprint(alph_numbered[19999:20010])

last_clean = []

for element in clean_data:
    element["LAST"] = element.get("NAME").split(" ")[-1]
    last_clean.append(element)

last_clean = sorted(last_clean,key=itemgetter("LAST"))

numlast = 0

last_alph = []

for element in last_clean:
    element["ALPHA"] = numlast
    numlast += 1
    last_alph.append(element)

pprint(last_alph[:10])
pprint(last_alph[19999:20010])

predic_data = []

#Create a prediction field that gives the results of our predicted model

for element in clean_data:
    element["PREDICTION"] = -40 + 0.8*element.get("WEALTH_INDEX") + 0.12*element.get("RFA_2F")
    predic_data.append(element)

predic_data = sorted(predic_data,key=itemgetter("PREDICTION"), reverse=True)

#print top 10 entries using our prediction

pprint(predic_data[:10])

#Get variable that represents ten % of entries

ten_percent = len(predic_data)/10

#pull records that represent to ten percent and bottom ten percent of our prediction

predic_top = predic_data[:ten_percent]
predic_bott = predic_data[ten_percent:]

#sum up the number of successful reponses for the top ten percent of predictions

top_target = 0
for element in predic_top:
    top_target += element.get("TARGET_B")

#sum up the number of successful reponses for the bottom ten percent of predictions

bott_target = 0
for element in predic_bott:
    bott_target += element.get("TARGET_B")

#Compare the proportion of respones for the top ten percent and the bottom ten percent

top_prop = float(top_target)/len(predic_top)
bott_prop = float(bott_target)/len(predic_bott)

#The top ten percent responded ~26% of the time, while the bottom ten percent responded ~4% of the time
#We know from above that the average response rate is ~6%
#Our model appears to have successfully indicated whether a user responds or not

print top_prop
print bott_prop

# <codecell>


