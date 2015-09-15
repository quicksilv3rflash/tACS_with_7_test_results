#So, I've recorded all my movements through the maze as a single GIANT LOG FILE.
#This program (besides making sure I know how to generate files in Python)
#will ensure that I have 30 little log files of movements, one for each maze.

#imports
import math

textfilemovearray = open("all_30_maze_move_logs_during_eeg_recording.txt", "r")
stringvariablemovearray = textfilemovearray.read()
giantstringindex = 19
for mazenumber in range(0,30):
    littlemovestring = "["
    while True:
        giantstringindex += 19
        littlemovestring = littlemovestring + (stringvariablemovearray[giantstringindex + 1:giantstringindex + 18])
        if(stringvariablemovearray[giantstringindex + 15:giantstringindex + 17] ==
           " 5"):
            break
        littlemovestring = littlemovestring + ", "

    littlemovestring = littlemovestring + "]"

    filename = "move"
    if(mazenumber < 10):
        filename = filename + "0"
    filename = filename + str(mazenumber)
    filename = filename + ".txt"

    outfile = open(filename,"w") #opens file with name of "moveXX.txt"
    #note: opening files with "w" flag auto-nukes previous contents :)
    outfile.write(littlemovestring)
    outfile.close()
    print("Slice complete. File write complete.")
