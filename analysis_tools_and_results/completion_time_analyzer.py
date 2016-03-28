#This program will generate a 5 number summary for all mazes in
#4 categories. These are:
#NOSTIM
#CTLSTIM
#MAZESTIM_X1
#MAZESTIM_X2

#imports
import math,os

#master lists of the stats to find the medians of
masterendtimes = []
masternonpathcells = []
masterwalltraversal = []

#set up os path to process each file
for file in os.listdir(os.getcwd() + "/testdata/all_lumped"):

    #load test data file
    textfiletestdata = open(os.getcwd() + "/testdata/all_lumped/" + file,"r")
    stringtestdata = textfiletestdata.read()
    textfiletestdata.close()


    #load test end times
    for x in range (0, len(stringtestdata)):
        if(stringtestdata[x-2:x] == " 5"):
            masterendtimes.append(int(stringtestdata[x-15:x-10]) - 10000)


mediantimes = []
for printvar in range (0, 30):
    mazeXXtimes = []
    sortedmazeXXtimes = []
    for scanvar in range (0, 11):
        mazeXXtimes.append(masterendtimes[printvar + 30*scanvar])
    sortedmazeXXtimes = sorted(mazeXXtimes)
    mediantimes.append(sortedmazeXXtimes[5])

    print("Median completion time for maze number " + str(printvar) + ":\n", mediantimes[printvar],"\n")

