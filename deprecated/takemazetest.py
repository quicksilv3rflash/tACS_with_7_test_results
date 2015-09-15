#This is the final version of the maze test administration program.
#Users will be led through the following pathway: ([X]=complete, [ ]=incomplete)
#[X] tACS device calibration
#[X] 30 mazes. Pathway shown to user on screen before test run.
#1/3 controlEEG, 1/3 mazeEEG, 1/3 nostim

#   all hail machine empire

#imports
import random, pygame, sys, math, time
from pygame.locals import *

#init stuff for pygame
pygame.init()
FPS = 30
fpsClock = pygame.time.Clock()
displaysurface = pygame.display.set_mode((1200, 650))
pygame.display.set_caption("tACS test administration program")
font = pygame.font.Font(None, 36)
#----==== GLOBAL VARIABLES ====----
#Yes, I know global variables are evil. I'm using them heavily in this code.

#cell: which cell are we in? (0 to 143)
global cell

#framecount: how many frames have passed
#since the beginning of the current maze? (starts at 10000)
global framecount

#mazearray: a description of the maze's wall locations.
global mazearray

#mazeimage: a 603 x 603 .png of the maze.
global mazeimage

#mazepath: a log of how to go through the maze.
global mazepath

#movearray: a log of how the user actually went through the maze.
global movearray

#controlstim: a list of RGB values to control the tACS device.
global controlstim

#mazestim: a list of RGB values to control the tACS device (1 per maze)
global mazestim

#----==== FUNCTIONS ====----

#getmazestim: load maze stimulation dataset
def getmazestim(whichmaze):
    global mazestim
    mazestim = []
    filepath = "donotopenbeforetest/stim"
    if(whichmaze < 10):
        filepath = filepath + "0"
    filepath = filepath + str(whichmaze) + ".txt"
    file = open(filepath,"r")
    mstmstr = file.read()
    file.close()
    for x in range(0,int(len(mstmstr)/5)):
        mazestim.append(int(mstmstr[1+(5*x):4+(5*x)]))


#getcontrolstim: load the control stimulation dataset.
def getcontrolstim():
    global controlstim
    controlstim = [] #must clear controlstim before appending to it.
    textfilecontrolstim = open("donotopenbeforetest/controlstim.txt","r")
    controlstring = textfilecontrolstim.read() #move data to string
    textfilecontrolstim.close() #close the file
    for x in range(0,901):#901 values are in controlstim.txt
        controlstim.append(int(controlstring[1+(5*x):4+(5*x)]))

#Performblinding: randomly assign nostim/controlstim/mazestim.
def performblinding():
    blindarray = []
    for x in range (0, 30): 
        blindarray.append(0)
#blindarray now has 30 zeroes.
#blindarray gets 10 of its zeroes replaced with 1s.
    controlstims = 0
    while(controlstims != 10): 
        whichcell = math.floor(random.random() * 30)
        if(blindarray[whichcell] == 0):
            controlstims += 1
            blindarray[whichcell] = 1
#blindarray gets 10 of its zeroes replaced with 2s.
    mazestims = 0
    while(mazestims != 10):
        whichcell = math.floor(random.random() * 30)
        if(blindarray[whichcell] == 0):
            mazestims += 1
            blindarray[whichcell] = 2
    return blindarray

#Getmazearray: load mazearray from file. Input: Which maze?
def getmazearray(whichmaze):
    global mazearray
    mazearray = [] #clear mazearray
    #set filename to donotopenbeforetest/mazeXX.txt
    filename = "donotopenbeforetest/maze"
    if(whichmaze < 10):
        filename = filename + "0"
    filename = filename + str(whichmaze)
    filename = filename + ".txt"
    #now we can actually open the text file containing the maze array.
    textfilemazearray = open(filename, "r") #refer to the file
    stringvariablemazearray = textfilemazearray.read() #move data to string
    textfilemazearray.close()
    for x in range (0, 144): #only for 12x12 mazes
    #must mangle mazeXX.txt back into an array of tuples.
        mazearray.append((int(stringvariablemazearray[2 + (11*x)]),
                          int(stringvariablemazearray[5 + (11*x)]),
                          int(stringvariablemazearray[8 + (11*x)])))
#so after all that we've reconstituted mazearray, as it left the maze generator.
#the format of mazearray, restated here to avoid confusion...
#(visited?, rightwall?, upperwall?) <-- a tuple like this for each cell
#Cells are numbered from bottom left to top right, for a 3x3 it looks like:
# 6 7 8
# 3 4 5
# 0 1 2
#Note that "visited?" is used by the recursive backtracking maze generation
#algorithm and unused everywhere after; I've left it in regardless.

#Getmazeimage: load maze image from file. Input: Which maze?
def getmazeimage(whichmaze):
    global mazeimage
    filename = "donotopenbeforetest/maze"
    if(whichmaze < 10):
        filename = filename + "0"
    filename = filename + str(whichmaze)
    filename = filename + ".png"
    #having crafted donotopenbeforetest/mazeXX.png filename, we open file.
    mazeimage = pygame.image.load(filename)
    
#Getmazepath: load maze traversal path from file. Input: which maze?
def getmazepath(whichmaze):
    global mazepath
    mazepath = [] #must clear mazepath before appending to it.
    filename = "donotopenbeforetest/move"
    if(whichmaze < 10):
        filename = filename + "0"
    filename = filename + str(whichmaze)
    filename = filename + ".txt"
    textfilemovearray = open(filename, "r")
    movestring = textfilemovearray.read()
    textfilemovearray.close()
    index = 0
    while True:
        mazepath.append((int(movestring[40+(19*index):45+(19*index)]),
                         int(movestring[47+(19*index):52+(19*index)]),
                         int(movestring[54+(19*index)])))
        if(int(movestring[54+(19*index)]) == 5):
            break
        index += 1

#celltoposition converts from a cell to a position in pixels.
def celltoposition(currentcell):
    xpixloc = 601 + (50 * (currentcell%12))
    ypixloc = 602 - (50 * math.floor(currentcell/12))
    return (xpixloc, ypixloc)

#Showpath: show the user the path through the maze. Input 1: which maze?
#Input 2: 0 = nostim, 1 = controlEEG, 2 = mazeEEG
#while not included yet, stimulation will go here...
def showpath(whichmaze, stimtype):

    getmazestim(whichmaze)
    global framecount
    framecount = 10000 #framecount starts at 10000.
    global cell
    cell = 0 #cell starts at 0.
    pathindex = 0 #keeps track of where we are in path playback
    getmazeimage(whichmaze) #load the image for the maze
    getmazepath(whichmaze)  #load the correct path for the maze
    #now the video display loop.
    while True:
        if(stimtype == 0):
            setoutputcurrent(127)
        if(stimtype == 1):
            setoutputcurrent(controlstim[framecount - 10000])
        if(stimtype == 2):
            setoutputcurrent(mazestim[framecount - 10000])
            
        displaysurface.blit(mazeimage, (575,25)) #blit mazeimage to surface
        circleposition = celltoposition(cell)
        pygame.draw.circle(displaysurface, (0,255,255),circleposition,20,0)
        pygame.display.update() #update display
        fpsClock.tick(FPS) #tick FPS clock
        framecount = framecount + 1
        if(cell == 143): #break if the maze is done.
            break
        if(framecount >= mazepath[pathindex][0]):
            pygame.event.get() #this must be done to prevent the
            #operating system from thinking the program has stopped responding.
            cell = mazepath[pathindex][1] - 10000
            pathindex += 1

#movecircle moves the circle. Takes integer input.
#0:right
#1:up
#2:left
#3:down
def movecircle(direction):
    global cell
    storemove(direction)
    if(validmove(cell, direction) == 1):
        if(direction == 0):
            cell = cell + 1
        if(direction == 1):
            cell = cell + 12
        if(direction == 2):
            cell = cell - 1
        if(direction == 3):
            cell = cell - 12

#validmove returns 1 if valid, 0 if invalid
def validmove(currentcell, direction):
#let's check for edges first. left edge?
    if((currentcell % 12 == 0) and (direction == 2)):
        return 0
    #right edge?
    if((currentcell % 12 == 11) and (direction == 0)):
        return 0
    #bottom edge?
    if((currentcell < 12) and (direction == 3)):
        return 0
    #top edge?
    if((currentcell > 131) and (direction == 1)):
        return 0
    #now let's check for actual maze walls...
    #right wall?
    if((direction == 0) and (mazearray[cell][1] == 1)):
        return 0
    #upper wall?
    if((direction == 1) and (mazearray[cell][2] == 1)):
        return 0
    #left wall?
    if((cell - 1) >= 0):
        if((direction == 2) and (mazearray[cell - 1][1] == 1)):
            return 0
    #bottom wall?
    if((cell - 12) >= 0):
        if((direction == 3) and (mazearray[cell - 12][2] == 1)):
            return 0
    return 1

#storemove stores test subjects' movements in movearray.
#movearray: when, where, how
def storemove(direction):
    global movearray
    global cell
    global framecount
    movearray.append((framecount, (cell+10000), direction))

#setoutputcurrent draws the rect object required to set the output
#note that this function *DOES NOT* actually update the display!
#how RGB value maps to current:
#RGB || Current
# 99 || -2mA
#113 || -1mA
#127 ||  0mA
#141 ||  1mA
#155 ||  2mA
def setoutputcurrent(RGB):    
    pygame.draw.rect(displaysurface, (RGB,RGB,RGB), (10,10,500,630),0)

#----==== THINGS THAT HAPPEN ONLY ONCE (OUTSIDE MAIN LOOP) ====----
#load controlstim
getcontrolstim()
#make sure movearray is empty and then add a timestamp to it
movearray = []
when = time.time()
when = str(when)
timestampstringlength = len(when)
if(timestampstringlength < 15):
    for x in range(0, (15 - timestampstringlength)):
        when = when + "_"
movearray.append(when)
#Get the random sequence of tests. (0 = nostim, 1 = controlstim, 2 = mazestim)
blindarray = performblinding()


#We start with maze number zero.
mazenumber = 0


#some text to help the user align the window / remind them to take tutorial
introtext = font.render("Welcome to the tACS experiment, [ HUMAN ]."
                        , 0,(255,0,0))
displaysurface.blit(introtext, (575, 25))
introtext = font.render("Please run tutorial.exe before using this program."
                        , 0,(255,0,0))
displaysurface.blit(introtext, (575, 60))
introtext = font.render("If you have not yet done so, please close this"
                        , 0,(255,0,0))
displaysurface.blit(introtext, (575, 95))
introtext = font.render("window. Otherwise, you may continue. Attach the"
                        , 0,(255,0,0))
displaysurface.blit(introtext, (575, 130))
introtext = font.render("photosensor to the screen and adjust the window"
                        , 0,(255,0,0))
displaysurface.blit(introtext, (575, 165))
introtext = font.render("so that this entire text area is visible, and the"
                        , 0,(255,0,0))
displaysurface.blit(introtext, (575, 200))
introtext = font.render("photosensor is in the center of the grey box to the"
                        , 0,(255,0,0))
displaysurface.blit(introtext, (575,235))
introtext = font.render("left of this text. Use aluminum foil, dark colored"
                        , 0,(255,0,0))
displaysurface.blit(introtext, (575, 270))
introtext = font.render("paper, or opaque tape to hide the grey box during"
                        , 0,(255,0,0))
displaysurface.blit(introtext, (575, 305))
introtext = font.render("testing. Attach electrodes to the tACS device,"
                        , 0,(255,0,0))
displaysurface.blit(introtext, (575, 340))
introtext = font.render("subject's head and upper back as described in the"
                        , 0,(255,0,0))
displaysurface.blit(introtext, (575, 375))
introtext = font.render("instructions supplied with this program and tACS"
                        , 0,(255,0,0))
displaysurface.blit(introtext, (575, 410))
introtext = font.render("device. Set the tACS device to CAL and turn it on."
                        , 0,(255,0,0))
displaysurface.blit(introtext, (575, 445))
introtext = font.render("Adjust coarse and fine controls to minimize the"
                        , 0,(255,0,0))
displaysurface.blit(introtext, (575, 480))
introtext = font.render("brightness of the red and blue LEDs in the tACS"
                        , 0,(255,0,0))
displaysurface.blit(introtext, (575, 515))
introtext = font.render("device. Set the tACS device to ZAP and press any"
                        , 0,(255,0,0))
displaysurface.blit(introtext, (575, 550))
introtext = font.render("key to begin the experiment."
                        , 0,(255,0,0))
displaysurface.blit(introtext, (575, 585))
font = pygame.font.Font(None, 15)
introtext = font.render("ALL HAIL MACHINE EMPIRE"
                        , 0,(25,0,0))
displaysurface.blit(introtext, (800, 617))
#set output to 0mA
setoutputcurrent(127)
pygame.display.update()
#hang while user aligns window
broken = 0
while True:
    for event in pygame.event.get():
        if(event.type == QUIT):
            pygame.quit()
            sys.exit()
        if(event.type == KEYDOWN):
            broken = 1
    if(broken == 1):
        break
#----==== MAIN LOOP ====----
while True:
    #show the user how to go through the maze
    showpath(mazenumber, blindarray[mazenumber])
    #get events so that user input during playback doesn't bleed into real run
    pygame.event.get()
    #add the maze number to the movearray
    stringmazedescriptor = "Maze Number: "
    if(mazenumber < 10):
        stringmazedescriptor = stringmazedescriptor + "0"
    stringmazedescriptor = stringmazedescriptor + str(mazenumber)
    movearray.append(stringmazedescriptor)
    #add the type of stimulation applied to the movearray
    stringstim = "tACS:"
    if(blindarray[mazenumber] == 0):
        stringstim = stringstim + "nostim   0"
    if(blindarray[mazenumber] == 1):
        stringstim = stringstim + "ctrlEEG  1"
    if(blindarray[mazenumber] == 2):
        stringstim = stringstim + "mazeEEG  2"
    movearray.append(stringstim)
#----==== USER INPUT / EVENT HANDLING LOOP ====----
    setoutputcurrent(127) #we reset the output to 0 during user movements
    framecount = 10000 #we reset the framecount before logging the user
    cell = 0 #we also reset the cell.
    getmazearray(mazenumber) #and we load "where the walls are"
    while True:
        #quit cleanly. The user input event handler lives here too.
        for event in pygame.event.get():
            if(event.type == QUIT):
                pygame.quit()
                sys.exit()
            if(event.type == KEYDOWN):
                if(event.key == K_RIGHT):
                    movecircle(0)
                if(event.key == K_UP):
                    movecircle(1)
                if(event.key == K_LEFT):
                    movecircle(2)
                if(event.key == K_DOWN):
                    movecircle(3)
        displaysurface.blit(mazeimage, (575, 25))
        circleposition = celltoposition(cell)
        pygame.draw.circle(displaysurface, (0,255,255),circleposition,20,0)
        pygame.display.update()
        fpsClock.tick(FPS)
        framecount = framecount + 1
        if(cell == 143):
            storemove(5)
            break
    #now that the user has run this maze we can begin the next one.
    mazenumber += 1
#later this will only be triggered after completion of maze29!
#of course, this is implemented by checking for mazenumber == 30...
    if(mazenumber == 30):
        outfile = "TESTDATA_"
        outfile = outfile + movearray[0]
        outfile = outfile + ".txt"
        testdata = open(outfile, "w")
        testdata.write(str(movearray))
        testdata.close()
        #set output to 0mA
        setoutputcurrent(127)
        font = pygame.font.Font(None, 70)
        exittext = font.render("TURN OFF tACS DEVICE"
                               , 0,(255,0,0))
        displaysurface.blit(exittext, (580, 230))
        exittext = font.render("THEN PRESS ANY KEY"
                               , 0,(255,0,0))
        displaysurface.blit(exittext, (580, 380))
        pygame.display.update()
        #hang while user deactivates tACS device
        broken = 0
        while True:
            for event in pygame.event.get():
                if(event.type == QUIT):
                    pygame.quit()
                    sys.exit()
                if(event.type == KEYDOWN):
                    broken = 1
            if(broken == 1):
                break
        pygame.quit()
        sys.exit()
