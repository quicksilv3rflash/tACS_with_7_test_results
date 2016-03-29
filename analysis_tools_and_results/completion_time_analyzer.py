#This program will generate a 5 number summary for all mazes in
#4 categories. These are:
#NOSTIM
#CTLSTIM
#MAZESTIM_X1
#MAZESTIM_X2

#imports
import math,os

#the median times. entered manually!
medianendtimes = [480,404,569,453,509,449,509,368,270,430,427,625,244,242,308,700,500,273,590,430,325,231,400,539,323,477,429,459,266,346]


#master lists of the stats to find the medians of
currentendtimes = []
currentstimtypes = []

deprecatedendtimes = []
deprecatedstimtypes = []


#set up os path to process each file (current testdata)
for file in os.listdir(os.getcwd() + "/testdata/current"):

    #load test data file
    textfiletestdata = open(os.getcwd() + "/testdata/current/" + file,"r")
    stringtestdata = textfiletestdata.read()
    textfiletestdata.close()


    #load test end times
    for x in range (0, len(stringtestdata)):
        if(stringtestdata[x-2:x] == " 5"):
            currentendtimes.append(int(stringtestdata[x-15:x-10]) - 10000)

    #load stim types
    for x in range (0, len(stringtestdata)):
        if(stringtestdata[x-4:x] == "tACS"):
            currentstimtypes.append(int(stringtestdata[x+10:x+11]))


#set up os path to process each file (deprecated testdata)
for file in os.listdir(os.getcwd() + "/testdata/deprecated"):

    #load test data file
    textfiletestdata = open(os.getcwd() + "/testdata/deprecated/" + file,"r")
    stringtestdata = textfiletestdata.read()
    textfiletestdata.close()


    #load test end times
    for x in range (0, len(stringtestdata)):
        if(stringtestdata[x-2:x] == " 5"):
            deprecatedendtimes.append(int(stringtestdata[x-15:x-10]) - 10000)

    #load stim types
    for x in range (0, len(stringtestdata)):
        if(stringtestdata[x-4:x] == "tACS"):
            deprecatedstimtypes.append(int(stringtestdata[x+10:x+11]))


#all NOSTIM times
normNOSTIMtimes = []
for x in range(0, 120):
    if(currentstimtypes[x] == 0):
        normNOSTIMtimes.append((currentendtimes[x])/(medianendtimes[x % 30]))
for x in range(0, 210):
    if(deprecatedstimtypes[x] == 0):
        normNOSTIMtimes.append((deprecatedendtimes[x])/(medianendtimes[x % 30]))

#all CTLSTIM times
normCTLSTIMtimes = []
for x in range(0, 120):
    if(currentstimtypes[x] == 1):
        normCTLSTIMtimes.append((currentendtimes[x])/(medianendtimes[x % 30]))
for x in range(0, 210):
    if(deprecatedstimtypes[x] == 1):
        normCTLSTIMtimes.append((deprecatedendtimes[x])/(medianendtimes[x % 30]))

#only CURRENT (fixed) MAZESTIM times
normMAZEX1times = []
for x in range(0, 120):
    if(currentstimtypes[x] == 2):
        normMAZEX1times.append((currentendtimes[x])/(medianendtimes[x % 30]))


#only DEPRECATED (broken) MAZESTIM times
normMAZEX2times = []
for x in range(0, 210):
    if(deprecatedstimtypes[x] == 2):
        normMAZEX2times.append((deprecatedendtimes[x])/(medianendtimes[x % 30]))

#sort the lists
sortedNOSTIM = sorted(normNOSTIMtimes)
sortedCTLSTIM = sorted(normCTLSTIMtimes)
sortedMAZEX1 = sorted(normMAZEX1times)
sortedMAZEX2 = sorted(normMAZEX2times)

print("NORMALIZED NOSTIM","\n")
print("MIN: ",sortedNOSTIM[0],"\n")
print("Q1: ",sortedNOSTIM[27],"\n")
print("MED: ",(sortedNOSTIM[54]+sortedNOSTIM[55])/2,"\n")
print("Q3: ",sortedNOSTIM[82],"\n")
print("MAX: ",sortedNOSTIM[109],"\n")
print("=========================================","\n")

print("NORMALIZED CTLSTIM","\n")
print("MIN: ",sortedCTLSTIM[0],"\n")
print("Q1: ",sortedCTLSTIM[27],"\n")
print("MED: ",(sortedCTLSTIM[54]+sortedCTLSTIM[55])/2,"\n")
print("Q3: ",sortedCTLSTIM[82],"\n")
print("MAX: ",sortedCTLSTIM[109],"\n")
print("=========================================","\n")

print("NORMALIZED MAZEX1","\n")
print("MIN: ",sortedMAZEX1[0],"\n")
print("Q1: ",(sortedMAZEX1[9]+sortedMAZEX1[10])/2,"\n")
print("MED: ",(sortedMAZEX1[19]+sortedMAZEX1[20])/2,"\n")
print("Q3: ",(sortedMAZEX1[29]+sortedMAZEX1[30])/2,"\n")
print("MAX: ",sortedMAZEX1[39],"\n")
print("=========================================","\n")

print("NORMALIZED MAZEX2","\n")
print("MIN: ",sortedMAZEX2[0],"\n")
print("Q1: ",(sortedMAZEX2[17]),"\n")
print("MED: ",(sortedMAZEX2[34]+sortedMAZEX2[35])/2,"\n")
print("Q3: ",(sortedMAZEX2[52]),"\n")
print("MAX: ",sortedMAZEX2[69],"\n")
print("=========================================","\n")
