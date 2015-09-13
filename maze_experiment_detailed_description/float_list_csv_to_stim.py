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

#import stuff
import math

#step 1: read in the values and populate an array with them
textfilestimarray = open("controlsignal_AF3_only.csv", "r")
stringstim = textfilestimarray.read()
textfilestimarray.close()
#I'm not exactly sure why .close() is important but now that one of my lists
#is >5megabytes long, if memory is the reason, it's quite important to remember
#"memory: important to remember" is the best comment in this file.
#\n is one character.

stimarray = []
workingstring = ""
for x in range(0,len(stringstim)):
    if(stringstim[x] != "\n"):
        workingstring = workingstring + stringstim[x]
    if(stringstim[x] == "\n"):
        stimarray.append(float(workingstring))
        workingstring = ""
#so now stimarray contains all the values of the original .csv file...
#it's a list of floats (samples, each 1/128 second after the previous)

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
x = -1
while True:
    x+=1    
    if(x == len(stimarray)):
        #note: this means stimarray[x] isn't in existence!
        break
    if(stimarray[x] == 0):
        del stimarray[x]
#We have now removed every 16th value, converting from 128 samples/second
#to 120 samples/second, which can be readily converted to 15 samples/second.

#The following code averages every 8 values to yield 15 samples/second.
finalvalues = []
count = 0
buffer = 0
for x in range(0,len(stimarray)):
    count += 1
    buffer += stimarray[x]
    if(count == 8):
        finalvalues.append(buffer/8)
        count = 0
        buffer = 0
if(buffer != 0): #This makes sure that even if the # of entries in
                 #processedvalues isn't divisible by 15, the last few won't
                 #get left out.
    finalvalues.append(buffer/count)

#We have now adjusted the sample rate to 15 samples/second. Let's center
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

#BUT this isn't long enough for maze #15, so we append a copy of it to itself.
#Maximum delta between values is 9. Intermediate value 121 is added to keep the
#delta of the splice within the range of the original.
controlsignalrecordedlength = len(finalvalues)
finalvalues.append(int(121))
for x in range(0,controlsignalrecordedlength):
    finalvalues.append(finalvalues[x])
#Now finalvalues is double the original length without a huge splice delta!


