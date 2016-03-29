#So, I've recorded all movements through the maze as a single GIANT LOG FILE.
#This program will produce the median values (using all test data, even deprecated)
#for each maze. The values analyzed to find medians will be:
#Completion time, Non-path cells traversed, and Attempted wall traversals
#these medians will then be used to normalize the data set to account for
#the different lengths of the mazes during analysis.

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

