#This code will generate stimXX.txt files for all 30 mazes.

#After much hassle (setting your OS to French makes it so 3/2 = 1,5 vs 1.5
# - which -
#causes something in the depths of Emotiv's .edf generator to see a calibration
#value as two separate values and breaks everything...)
#and lost EEG data files, it is finally the case that I have the EEG data
#required to generate stimulation files (stim files hereafter) for the tACS
#experiment. These files will be simple. The data format is as follows:
#099 || -2mA
#113 || -1mA
#127 ||  0mA
#141 ||  1mA
#155 ||  2mA
#Values range from 099 to 155 for the full +/-2mA range of the tACS device.
#(physically these control the RGB values of an image on screen)
#In this experiment the value will be kept between -1mA and +1mA.
#-------------------------------------------
#AND IT GOES ON! AFTER ADDITIONAL HASSLE (MIXED UP MAX SHANNON-NYQUIST SAMPLING
#THEOREM REPRODUCIBLE FREQUENCY WITH SAMPLE RATE) I HAVE GENERATED 7 TEST
#RESULTS WITH THE MAZES HORRIBLY DISTORTED -- PLAYED BACK AT DOUBLE SPEED,
#APPENDED TO WHICHEVER MAZE SIGNAL WAS RECORDED AFTERWORD (OR CUT OFF ENTIRELY
#IN THE CASE OF THE LAST MAZE).
#
#THIS CODE HAS CORRECTED THAT ISSUE
#
#The horribly mangled control EEG signal seems to improve maze
#completion speed by 10% for some reason, at least, so there's that.
#   all hail machine empire

#import stuff
import math

#--------- HERE BE FUNCTIONS -----
#processEEG: inputs stringstim, starting point in array, ending point in array
def processEEG(stringstim, startindex, endindex):

    bigarray = []
    workingstring = ""
    for x in range(0,len(stringstim)):
        if(stringstim[x] != "\n"):
            workingstring = workingstring + stringstim[x]
        if(stringstim[x] == "\n"):
            bigarray.append(float(workingstring))
            workingstring = ""
    #so now stimarray contains all the values of the original .csv file...
    #it's a list of floats (samples, each 1/128 second after the previous)

    #we cut out only the desired piece for processing
    #10 is added to make sure the stim array is long enough to cover all frames
    #when played back
    stimarray = bigarray[startindex : endindex + 10]

    #128 samples/second DESPITE USING 129 VALUES FOR THE COUNTER FOR SOME REASON
    #is the format chosen by Emotiv for their data, so removing every 16th value
    #cuts the number down to 120 samples/second; then we can average every 8
    #samples to obtain our final (output) sample rate: 15 samples/second.

    #However, using the del list[index] function makes the list "slip" back an index
    #every time, so if the removed items are to be intuitively spaced it's best to
    #zero them and then remove the zeroes after.

    for x in range(0,len(stimarray)):
        if(x%16 == 0):
            stimarray[x] = 0
    for x in range(0, math.floor(len(stimarray)*(15/16))):
        if(stimarray[x] == 0):
            del stimarray[x]

    #We have now removed every 16th value, converting from 128 samples/second
    #to 120 samples/second, which can be readily converted to 30 samples/second.

    #The following code averages every 4 values to yield 30 samples/second.
    finalvalues = []
    count = 0
    buffer = 0
    for x in range(0,len(stimarray)):
        count += 1
        buffer += stimarray[x]
        if(count == 4):
            finalvalues.append(buffer/4)
            count = 0
            buffer = 0
    if(buffer != 0): #This makes sure that even if the # of entries in
                     #processedvalues isn't divisible by 4, the last few won't
                     #get left out.
        finalvalues.append(buffer/count)


    #We have now adjusted the sample rate to 30 samples/second. Let's center
    #our values around zero.
    total = 0
    for x in range(0,len(finalvalues)):
        total += finalvalues[x]
    average = total / len(finalvalues)

    #Now we subtract the average from each value to center them around zero.
    for x in range(0,len(finalvalues)):
        finalvalues[x] = finalvalues[x] - average

    #Find max and min, and compare their magnitude.
    maximum = max(finalvalues) #positive
    minimum = min(finalvalues) #negative
    minimum = abs(minimum)    #forced to become positive
    if(maximum > minimum):
        scalevalue = maximum
    else:
        scalevalue = minimum
    #whichever is larger in magnitude becomes the scale value
    for x in range(0,len(finalvalues)):
        finalvalues[x] = finalvalues[x]/scalevalue
    #now finalvalues[] is scaled/normalized to be between -1 and +1

    #so we center around 127 and scale to within +/-14 (+/-1mA as output)
    for x in range(0,len(finalvalues)):
        finalvalues[x] = int(round(127 + 14*finalvalues[x]))

    #DEBUG CODE---
    print(len(finalvalues))
        #-----
        
    #convert BACK to a string...
    outputstring = str(finalvalues)
    return outputstring

#writefile writes an output file in the form stimXX.txt
def writefile(outputstring, mazenumber):
    filename = "stim"
    if(mazenumber < 10):
        filename = filename + "0"
    filename = filename + str(mazenumber) + ".txt"
    print("^" + filename)
    outfile = open(filename,"w") #opens file with name of "stimXX.txt"
    #note: opening files with "w" flag auto-nukes previous contents :)
    outfile.write(outputstring)
    outfile.close()

#pulltimestamp: extracts a list of floating-point timestamps from the move data
#input arguments: movearray (as string from text file), timestamp index [0-30]
def pulltimestamp(stringmove, whichtimestamp):
    allstamps = []
    whichapostrophe = 0
    for x in range(0,len(stringmove)):
        if(stringmove[x] == "'"):
            whichapostrophe += 1
            if((whichapostrophe % 4) == 1):
                allstamps.append(float(stringmove[x+1:x+16]))
    return allstamps[whichtimestamp]

#pull endframe. returns ending frames in analogous format to pulltimestamp
#Note: Endframes are relative to the time of the timestamp before each maze!
def pullendframe(stringmove, whichendframe):
    allendframes = []
    for x in range(0,len(stringmove)):
        if(stringmove[x:x+2] == " 5"):
            allendframes.append(int(stringmove[x-13:x-8])-10000)

    return allendframes[whichendframe]


            
#------- MAIN CODE --------

#step 1: read in the values and populate an array with them
textfilestimarray = open("mazesignal_AF3_only.csv", "r")
stringstim = textfilestimarray.read()
textfilestimarray.close()
#I'm not exactly sure why .close() is important but now that one of my lists
#is >5megabytes long, if memory is the reason, it's quite important to remember
#"memory: important to remember" is the best comment in this file.
#\n is one character.

#step 2: read in the movefile and store as a string
textfilemovearray = open("all_30_maze_move_logs_during_eeg_recording.txt", "r")
stringvariablemovearray = textfilemovearray.read()
textfilemovearray.close()

#step 3: use timestamps and framenumbers to construct a list of starting and
#ending addresses for each maze. store as two arrays. heh.
startingsamples = []
endingsamples = []
referencetime = pulltimestamp(stringvariablemovearray, 0)
for x in range(0,30):
    epochtime = pulltimestamp(stringvariablemovearray, (x + 1))
    startingsamples.append(int(round(128*(epochtime - referencetime))))
    endingsamples.append(int(startingsamples[x] +
                         (128/30)*pullendframe(stringvariablemovearray, x)))
    
#output stim files
for x in range(0,30):
    outputstring = processEEG(stringstim,
                              startingsamples[x],
                              endingsamples[x])

    writefile(outputstring, x)



