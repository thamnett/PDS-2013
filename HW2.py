# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

#import matplotlib
%pylab inline

import matplotlib.pyplot as plt

#read in survey data
survey = open("survey.csv", "r")

#create list to store survey data
data = []

#convert lines in survey data into a list, removing commas delimiting the values
for line in survey:
    parts = line.strip().split(',')
    data.append(parts)

#close the file
survey.close()

#create a translation dictionary of skill level to numbers, for plotting later on    
dict2_trun = {'I don\xe2\x80\x99t even understand the question':1,
'I have no experience working in a terminal ':2, 
'I have issued a few commands in a terminal based on given instructions ': 3,
'I have written simple terminal commands or done some system work on the terminal ':4,
'I have written complex commands done or have done deep system work  ':5}
dict3_trun = {'I have never directly accessed a database ':1,
'I have issued simple queries to a relational database based on given instructions ':2,
'I can write simple queries and issue them to a database ':3,
'I can write very complex queries when needed ':4,
'I am a database hacker ':5}
dict4_trun = {'I have never programmed before.':1,
'I have written simple programs based on instructions or a tutorial':2,
'I can write simple programs to accomplish tasks I encounter':3,
'I can write complex programs am familiar with programming design patterns software testing system design and algorithms.':4,
'I am a hacker or have  senior-level programming experience':5}

#create dictionaries to store the responses and counts of responses
dict2 = {}
dict3 = {}
dict4 = {}

#for each sublist withtin the data (each line), if the response is in the dictionary
#increase the count by one, otherwise, add the response to the dictionary with
#a count of one
for element in data:
    if element[2] in dict2:
        dict2[element[2]] += 1
    else:
        dict2[element[2]] = 1
    
    if element[3] in dict3:
        dict3[element[3]] += 1
    else:
        dict3[element[3]] = 1

    if element[4] in dict4:
        dict4[element[4]] += 1
    else:
        dict4[element[4]] = 1

#create lists to prepare data counts for display
ls2 = []
ls3 = []
ls4 = []

#create a list of lists, sorted by the skill level
#by translating skill level to a number using the translation dict
#we created above
for w in sorted(dict2_trun, key=dict2_trun.get):
    try:
        ls2.append([dict2_trun.get(w), dict2[w]])
    except KeyError:
        ls2.append([dict2_trun.get(w), 0])

for w in  sorted(dict3_trun, key=dict3_trun.get):
    try:
        ls3.append([dict3_trun.get(w), dict3[w]])
    except KeyError:
        ls3.append([dict3_trun.get(w), 0])

for w in  sorted(dict4_trun, key=dict4_trun.get):
    try:
        ls4.append([dict4_trun.get(w), dict4[w]])
    except KeyError:
        ls4.append([dict4_trun.get(w), 0])

#create x coordinate and y corrdinate lists to prepare for charting
x2 = []
y2 = []
x3 = []
y3 = []
x4 = []
y4 = []

#the first element in each sublist is the x value, second is the y value
for element in ls2:
    x2.append(element[0])
    y2.append(element[1])

for element in ls3:
    x3.append(element[0])
    y3.append(element[1])
    
for element in ls4:
    x4.append(element[0])
    y4.append(element[1])

#plot the results with skill level on x axis and count on y axis
#and print the translation dicts
plt.plot(x2,y2)
plt.axis([1, 5, 0, 25])
plt.show()
print dict2_trun

plt.plot(x3,y3)
plt.axis([1, 5, 0, 25])
plt.show()
print dict3_trun

plt.plot(x4,y4)
plt.axis([1, 5, 0, 25])
plt.show()
print dict4_trun

#show all three on one chart, creating labels for the legend
plt.plot(x2,y2, label='Terminal')
plt.plot(x3,y3, label='Database')
plt.plot(x4,y4, label='Programming')
plt.axis([1, 5, 0, 30])
legend()
plt.show()

#plot like above, but now a bar chart format
plt.bar(x2,y2)
plt.axis([1, 6, 0, 25])
plt.show()
print dict2_trun

plt.bar(x3,y3)
plt.axis([1, 6, 0, 25])
plt.show()
print dict3_trun

plt.bar(x4,y4)
plt.axis([1, 6, 0, 25])
plt.show()
print dict4_trun

# <codecell>

#create dict structure to store answers and modifiers
edumod = {'1':-3.0,'2':-1.0,'3':0.0,'4':1.0,'5':3.0,'6':4.0}
occmod = {'1':2.5,'2':0.6,'3':0.0,'4':0.2,'5':-0.5,'6':-1.5,'7':0.3,'8':0.8,'9':-2.5}

#open the data file we created after removing all NA records
#note: working off of the marketing data stripped of NAs from HW1 called "noNA.data.txt"
incdat = open("noNA.data.txt", "r")

edmoddiff = 0.0
twofacmoddiff = 0.0
numlin = 0.0
simpdiff = 0.0
twofacdiff = 0.0

#create list to read in data
inclst = []

#append file data to list
for lines in incdat:
    columns = lines.split()
    inclst.append(columns)

#close file
incdat.close()

#for every line in list, track the following:
#modified income using simple model
#modified income using the two factor model
#total number of lines (responses)
#number of overestimates and underestimates using simple model
#number of overestimates and underestimates using two factor model
for lines in inclst:
        edmodnum = edumod.get(lines[4]) + 4.0 - float(lines[0])
        edmoddiff += abs(edmodnum)
        twofacmodnum = occmod.get(lines[5]) + edumod.get(lines[4]) + 4.0 - float(lines[0])
        twofacmoddiff += abs(twofacmodnum)
        numlin += 1
        if edmodnum > 0:
            simpdiff += 1
        elif edmodnum < 0:
            simpdiff += -1
        if twofacmodnum > 0:
            twofacdiff += 1
        elif twofacmodnum < 0:
            twofacdiff += -1
    
#calculate average difference using simple model

avgeddiff = edmoddiff / float(numlin)

if simpdiff > 0:
    print "Simple model overestimates income by %i instances" % simpdiff
elif simpdiff < 0: 
    print "Simple model underestimates income by %i instances" % -simpdiff
else:
    print "Simple model equally over and underestimates income"

#print simple model results
print "Total difference in the simple model is %f" % edmoddiff
print "Avg difference in the simple model is %f" % avgeddiff

#calculate total difference and average difference using two factor model
avgdifftwofac = twofacmoddiff / float(numlin)

if twofacdiff > 0:
    print "Two factor model overestimates income by %i instances" % twofacdiff
elif twofacdiff < 0: 
    print "Two factor model underestimates income by %i instances" % -twofacdiff
else:
    print "Two factor model equally over and underestimates income"

#print two factor model results
print "Total difference in the two factor model is %f" % twofacmoddiff
print "Avg difference in the two factor model is %f" % avgdifftwofac

if avgdifftwofac > avgeddiff:
    print "Simple model predicts better than two factor model"
elif avgdifftwofac < avgeddiff:
    print "Two factor model predicts better than simple model"
else:
    print "Simple model and two factor model predict equally well"

# <codecell>


# <codecell>


