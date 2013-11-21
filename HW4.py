# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

#Q1
#First query to check that there are no duplicate shops
#SELECT shopcount FROM (SELECT COUNT(shop_id)AS shopcount FROM shops GROUP BY shop_id) AS cnt_qry WHERE shop_id > 1

#Query to get number of shops
#SELECT COUNT(shop_id)AS shopcount FROM shops 
#shopcount
#46426

#Q2
#SELECT AVG(price/100)AS avgprice FROM listings
#avgprice
#35.2175

#SELECT AVG(price)AS avgprice FROM transactions
#avgprice
#20.7581

#Q3
#SELECT AVG(lstprice)AS avglstprice FROM (SELECT price / quantity AS lstprice FROM transactions) AS lstpriceqry
#avglstprice
#20.45
#This is lower than the average listing price (< 2/3 of avg listing price)

#Q4
#SELECT AVG(lstprice)AS avglstprice FROM (SELECT price / quantity AS lstprice FROM transactions WHERE price > 0 and quantity > 0) AS lstpriceqry
#avglstprice
#20.50935394
#Slightly higher than average transaction listing price (by ~6 cents)

#Q5
#SELECT listing_id, price FROM listings ORDER BY price DESC LIMIT 5
#listing_id	price
#929296	25000000
#825605	3500000
#149300	2000000
#92558	1100000
#65276	1000000

#Q6
#SELECT buyer_user_id, COUNT(listing_id) AS listct FROM transactions GROUP BY buyer_user_id LIMIT 10
#I interpreted this as counting the distinct number of listings purchased by each buyer
#buyer_user_id	listct
#11	1
#21	1
#24	1
#37	1
#51	1
#52	1
#58	1
#59	1
#63	1
#90	1

#Q7
#SELECT lstct, COUNT(buyer_user_id) AS userct FROM (SELECT buyer_user_id, COUNT(listing_id) AS lstct FROM transactions
#GROUP BY buyer_user_id) AS lstqry GROUP BY lstct LIMIT 10
#lstct	userct
#1	78371
#2	6427
#3	850
#4	182
#5	52
#6	29
#7	17
#8	9
#9	4
#10	2

#Q8
#SELECT gender, COUNT(user_id) FROM users GROUP BY gender
#gender	count(user_id)
#female	36052
#male	6863
#private	52228

#Q9
#SELECT gender, COUNT(buyer_user_id) AS purchusr FROM users RIGHT OUTER JOIN (SELECT buyer_user_id FROM transactions GROUP BY buyer_user_id) AS purchusrqry 
#ON users.user_id = purchusrqry.buyer_user_id GROUP BY gender
#gender	purchusr
#\N	77337
#female	3274
#male	602
#private	4734


import re
import urllib
sock = urllib.urlopen("http://people.stern.nyu.edu/ja1517/data/pds_2012_roster.html")
htmlSource = sock.read()
sock.close()
#print htmlSource

netids = []

for line in htmlSource.split("<TR>"):
    result = re.search(".edu>(.*)</a>", line)
    if result:
        netids.append(result.group(1))
    else:
        pass

print netids
    
fourlstnet = []

for line in htmlSource.split("<TR>"):
    result = re.search(".edu>(.*)</a>", line)
    last = re.search("SCIENCE'>(\w{1,4}), ", line)
    if last:
        if result:
            fourlstnet.append(result.group(1))
        else:
            pass
    else:
        pass

print fourlstnet

print len(netids) - len(fourlstnet)

for line in htmlSource.split("<TR>"):
    studid = re.search(".edu>(.*)</a>", line)
    name = re.search("SCIENCE'>(.*)</a>&nbsp;", line)
    if name:
        fullname = name.group(1)
        last = re.search("(.*),", fullname)
        first = re.search(",(.*)", fullname)
        lastname = last.group(1)
        firstname = first.group(1)
        midtest = re.search("/s", firstname)
        idval = studid.group(1)
        if midtest:
            firstmid = re.search("(.*) ", firstname)
            middle = re.search(" (.*)", firstname)
            fisrtmidnm = firstmid.group(1)
            middlenm = middle.group(1)
            print firstmidnm, middlenm, "/t", lastname, "\t", idval
        else:
            print firstname, "\t", lastname, "\t", idval
    else:
        pass


for line in htmlSource.split("<TR>"):
    result = re.search(".edu>(.*)</a>", line)
    if result:
        subline = re.sub(".edu>(.*)</a>", r".edu>\1@stern.nyu.edu</a>", line)
        print subline.strip("\n")
    else:
        print line.strip("\n")

# <codecell>


