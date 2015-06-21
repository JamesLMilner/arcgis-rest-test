__author__ = 'JMilner'

import json
import csv
import urllib2
import datetime
import time
import os

ABSOLUTE_PATH = r"C:\Users\achiu\Documents\StatsOutput"
OUTPUT_CSV = "EsriUKContent.csv"

os.chdir(ABSOLUTE_PATH)

ids  = ["0895f24cf85b4251990a24305447ded7?",
	"7561029c176d43d09a5aa1180ada309a?",
	"cba7d9f4c1d84d1793058ed63f7cfa6d?",
        "d01fed57640b425aa77ceb605b01f6d8?",
        "e09ec4c77cc347d38629bc882056e3a3?",
        "29adce88e56647bca1c91aaea19e1361?",
        "43fd5c64b3f741a880efe6589f834f87?",
        "73f869e81a3f47d59bb632169728477e?",
        "e1df83515cfd4420962fad9a5ea229e6?",
        "ed2fcf4283ef44a682b4888c69f16408?"]

print "Current working directory: " + os.getcwd()
print os.getcwd() + "\\" + OUTPUT_CSV

csvrowwrite = [["id","views","size","type", "date","time"]]


for id in ids:
    url = "http://arcgis.com/sharing/rest/content/items/" + id +  "f=json"
    response = urllib2.urlopen(url)

    jsonpayload = json.load(response)
    print "payload recieved"
    numviews = jsonpayload["numViews"]
    fcsize = jsonpayload["size"]
    fctype = jsonpayload["type"]

    thedate = datetime.date.today()

    timestring = str(datetime.datetime.now().time())
    timestring = timestring[:timestring.index('.')]
    datestring = str(thedate.strftime('%m/%d/%y'))

    csvrow = id +","+ str(numviews) +","+ str(fcsize) + "," + str(fctype) + "," + datestring  +" "+ timestring #+ "\n"
    csvrowlist = [id, str(numviews), str(fcsize), str(fctype), datestring, timestring]
    csvrowwrite.append(csvrowlist)
    print "Creating Row"

with open(OUTPUT_CSV, 'wb') as fp:
    print "Writing to: " + os.path.abspath("import.csv")
    print "Writing rows..."
    a = csv.writer(fp, delimiter=',')
    a.writerows(csvrowwrite)

