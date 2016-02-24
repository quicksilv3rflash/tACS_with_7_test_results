#So, I've recorded all movements through the maze as a single GIANT LOG FILE.
#This program will produce the median values (using all test data, even deprecated)
#for each maze. The values analyzed to find medians will be:
#Completion time, Non-path cells traversed, and Attempted wall traversals
#these medians will then be used to normalize the data set to account for
#the different lengths of the mazes.

#imports
import math,os


masterendtimes = []

#load master file
textfilemovearray = open("maze_experiment_detailed_description/all_30_maze_move_logs_during_eeg_recording.txt", "r")
stringvariablemovearray = textfilemovearray.read()
textfilemovearray.close()

stimtypes = []

FinalNostim = 0
FinalCtlstim = 0
FinalMazestim = 0

#load the master end times
for x in range (0, len(stringvariablemovearray)):
    if(stringvariablemovearray[x-2:x] == " 5"):
        masterendtimes.append(int(stringvariablemovearray[x-15:x-10]) - 10000)
    #masterendtimes now contains end times of the prototype maze traversals



ctlstimtotal = 0
nostimtotal = 0
mazestimtotal = 0
    
#set up os path to process each file

for file in os.listdir(os.getcwd() + "/testdata/all_lumped"):

    normnostim = 0
    normctlstim = 0
    normmazestim = 0

    #load test data file
    textfiletestdata = open(os.getcwd() + "\\testdata\\all_lumped\\" + file,"r")
    stringtestdata = textfiletestdata.read()
    textfiletestdata.close()

    #later there will be a lot of different test end times, not just one.

    testendtimes = []
    normalizedtestendtimes = []


    #load test end times
    for x in range (0, len(stringtestdata)):
        if(stringtestdata[x-2:x] == " 5"):
            testendtimes.append(int(stringtestdata[x-15:x-10]) - 10000)
            
    #load stim types
    for x in range(0,len(stringtestdata)):
        if(stringtestdata[x-4:x] == "tACS"):
            stimtypes.append(int(stringtestdata[x+10]))


    #normalize the test end times
    for x in range(0, len(masterendtimes)):
        normalizedtestendtimes.append(testendtimes[x]/masterendtimes[x])


    for x in range(0,30):
        if(stimtypes[x] == 0):
            nostimtotal += normalizedtestendtimes[x]
        if(stimtypes[x] == 1):
            ctlstimtotal += normalizedtestendtimes[x]
        if(stimtypes[x] == 2):
            mazestimtotal += normalizedtestendtimes[x]

    normnostim = nostimtotal/nostimtotal
    normctlstim = ctlstimtotal / nostimtotal
    normmazestim = mazestimtotal / nostimtotal
    FinalNostim += normnostim
    FinalCtlstim += normctlstim
    FinalMazestim += normmazestim

print("normalized times with no stimulation\n", (FinalNostim/2),"\n")
print("normalized times with control stimulation\n",(FinalCtlstim/2),"\n")
print("normalized times with maze EEG stimulation\n",(FinalMazestim/2),"\n")
