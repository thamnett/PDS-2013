# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import matplotlib.pyplot as plt
import numpy as np
import json
import operator
from pprint import pprint

#read in data as a list of json dicts

data = []
with open('user_tag_activity.json', 'r') as f:
    for line in f:
        data.append(json.loads(line))

clean_data = []

#if any value in the json dict is NULL, ignore; otherwise, add to the clean data

for line in data:
    x = 0
    for vals in line.itervalues():
        if vals == 'NULL':
            x += 1
        else:
            pass
    if x == 0:
        clean_data.append(line)
    else:
        pass
    


user_set = set()
object_set = set()
response_set = set()

#create sets to count unique values in the total data

for line in data:
    user_set.add(line.get("user"))
    object_set.add(line.get("object"))
    response_set.add(line.get("response"))

print "The unique number of users is %i" % len(user_set)
print "The unique number of objects is %i" % len(object_set)
print "The unique number of responses is %i" % len(response_set)

accept_user = {}
reject_user = {}
count_user = {}
accept_response = {}
reject_response = {}
count_response = {}

#count the various rejects and accepts by user and response 
#in the clean data and store in dicts

for line in clean_data:
    
    if line.get("user") in count_user:
        count_user[line.get("user")] += 1 
    else:
        count_user[line.get("user")] = 1
    
    if line.get("accepted") == "0":
        if line.get("user") in reject_user:
            reject_user[line.get("user")] += 1
        else:
            reject_user[line.get("user")] = 1
    elif line.get("accepted") == "1":
        if line.get("user") in accept_user:
            accept_user[line.get("user")] += 1
        else:
            accept_user[line.get("user")] = 1
    else:
        pass
    
    if line.get("response") in count_response:
        count_response[line.get("response")] += 1
    else:
        count_response[line.get("response")] = 1
    
    if line.get("accepted") == "0":
        if line.get("response") in reject_response:
            reject_response[line.get("response")] += 1
        else:
            reject_response[line.get("response")] = 1
    elif line.get("accepted") == "1":
        if line.get("response") in accept_response:
            accept_response[line.get("response")] += 1
        else:
            accept_response[line.get("response")] = 1
    else:
        pass

rejrate_user = {}
accrate_user = {}
rejrate_response = {}

#calculate the rejection and acceptance rates for users and responses as dicts

for key, value in reject_user.iteritems():
    rejrate_user[key] = value / float(count_user.get(key))

for key in count_user.iterkeys():
    if accept_user.get(key) == None:
        accrate_user[key] = 0
    else:
        accrate_user[key] = accept_user.get(key) / float(count_user.get(key))
    
for key, value in reject_response.iteritems():
    rejrate_response[key] = value / float(count_response.get(key))

rejlst_user = []
acclst_user = []
rejratelst_user = []
accratelst_user = []
rejratelst_response = []

#sort the dicts into lists to find the largest values

rejlst_user = sorted(reject_user.iteritems(), key=operator.itemgetter(1), reverse = True)
acclst_user = sorted(accept_user.iteritems(), key=operator.itemgetter(1), reverse = True)
rejratelst_user = sorted(rejrate_user.iteritems(), key=operator.itemgetter(1), reverse = True)
accratelst_user = sorted(accrate_user.iteritems(), key=operator.itemgetter(1), reverse = True)
rejratelst_response = sorted(rejrate_response.iteritems(), key=operator.itemgetter(1), reverse = True)

#calculate the false positives ("red herrings") by exclusing the top rejections and acceptances

response_redherr = 0
for item in rejratelst_response[0:5]:
    if accept_response.get(item[0]) == None:
        pass
    else:
        response_redherr += int(accept_response.get(item[0]))
        
accept_redherr = 0
for item in acclst_user[0:5]:
    if reject_user.get(item[0]) == None:
        pass
    else:
        accept_redherr += int(reject_user.get(item[0]))

#print results of top 5 rates and counts, and the false positives by exclusing them
#note: for the rates, more than five have 100% rejection rates

print "\nThe 5 users with the highest rejection rates are: \n%s" % "\n".join(map(str, rejratelst_user[0:5]))
print "\nThe 5 users with the highest rejections are: \n%s" % "\n".join(map(str, rejlst_user[0:5]))
print "\nThe 5 responses with the highest rejection rates are: \n%s" % "\n".join(map(str, rejratelst_response[0:5]))
print "\nIf we were to try to automate the rejection process by rejecting the these responses,"
print " %i good (accepted) tags would erroneously be rejected" % response_redherr
print "\nThe 5 users with the highest acceptances are: \n%s" % "\n".join(map(str, acclst_user[0:5]))
print "\nIf one were to always accept responses from these users," 
print "%i bad tags would erroneously be accepted" % accept_redherr

#create a list from the sorted accpetance rates to prepare for plotting

accrate_plot = []
for line in accratelst_user:
    accrate_plot.append(line[1])
    
#plot distribution rates, from largest to smallest

plt.plot(accrate_plot)
plt.ylim(ymin = -.2)
plt.ylim(ymax = 1.2)
plt.show()

f.close()

#OUTPUT
#The unique number of users is 15699
#The unique number of objects is 340423
#The unique number of responses is 69871

#The 5 users with the highest rejection rates are: 
#(4461917972885738830L, 1.0)
#(7140081293236426261L, 1.0)
#(355792772524603626L, 1.0)
#(8968607845247884239L, 1.0)
#(355793772630603943L, 1.0)

#The 5 users with the highest rejections are: 
#(5461918972760738536L, 6009)
#(3461916972872738871L, 3606)
#(6400038450057764L, 2449)
#(4814036714632610472L, 2275)
#(-2088598916602095351L, 1517)

#The 5 responses with the highest rejection rates are: 
#(3345983059650407634L, 1.0)
#(5455263844942354374L, 1.0)
#(-7844519533094611714L, 1.0)
#(-8333402000801615613L, 1.0)
#(-2880596111102578955L, 1.0)

#If we were to try to automate the rejection process by rejecting the these responses,
#0 good (accepted) tags would erroneously be rejected

#The 5 users with the highest acceptances are: 
#(3461916972869738765L, 33628)
#(5461918972760738536L, 26302)
#(4814036714632610472L, 19007)
#(6400038450057764L, 17037)
#(8461920972786738646L, 11472)

#If one were to always accept responses from these users, 
#12391 bad tags would erroneously be accepted

# <codecell>


