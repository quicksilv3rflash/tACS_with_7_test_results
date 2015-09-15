#This program will display the mazes 0 - 29 onscreen.
#The user will be able to move a circle which spawns in the bottom-left
#corner of the maze to the top-right corner. The user will repeat this 5 times
#for each maze as practice, and then the sixth time will generate a record of
#movements with corresponding timestamps and frame numbers.
#   all hail machine empire


#imports
import random, pygame, sys, math, time
from pygame.locals import *

#init stuff for pygame
pygame.init()
FPS = 30
fpsClock = pygame.time.Clock()
displaysurface = pygame.display.set_mode((1200, 650))

#recording: are we recording this traversal?
global recording

#mazerun_number: how many times have we run this particular maze?
global mazerun_number
#we record the 6th run and start counting at 0.
mazerun_number = 5

#timestamp will be loaded with the current time when necessary
global timestamp

#mazeimage: the maze image blitted to the display screen
global mazeimage

#framecount will be the timebase for recording user input.
global framecount
framecount = 10000 #starting at 10000 so it will *probably* be 5 digits

#cell: where the circle's position is. starts in maze cell 0.
global cell
cell = 0

#movearray: stores test subjects' movements.
#format of movearray: (when?, where?, how?) ... that is,
#(current framecount, current cell, attempted move direction)
global movearray
movearray = []

#"mazearray" will actually contain the array as it was
#populated by the maze generator
global mazearray
mazearray = []


#-----====== HERE BE FUNCTIONS =====-----
#openmaze loads the required maze files.
def openmaze(whichmaze):
    global mazearray
    mazearray = [] #must clear mazearray before appending more stuff to it!
    global mazeimage
    #set filename to mazetest_n_dev/mazeXX.png
    filename = "donotopenbeforetest/maze"
    if(whichmaze < 10):
        filename = filename + "0" + str(whichmaze)
    else:
        filename = filename + str(whichmaze)
    filename = filename + ".png"
    #load the maze image.
    mazeimage = pygame.image.load(filename)
    #set filename to mazetest_n_dev/mazeXX.txt
    filename = "donotopenbeforetest/maze"
    if(whichmaze < 10):
        filename = filename + "0" + str(whichmaze)
    else:
        filename = filename + str(whichmaze)
    filename = filename + ".txt"
    #open/refer to the file
    textfilemazearray = open(filename ,'r')
    #actually transfer the file into a variable (a string) we can work with
    stringvariablemazearray = textfilemazearray.read()
    for x in range(0,144): #just 12x12 mazes here, sir
    #BUT we've got to mangle the string back into an array of tuples!
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

#celltoposition converts from a cell to a position in pixels.
def celltoposition(currentcell):
    xpixloc = 601 + (50 * (currentcell % 12))
    ypixloc = 602 - (50 * math.floor(currentcell / 12))
    return (xpixloc, ypixloc)

#timestampmazestamp is called immediately after beginning a maze.
#It says what time (in unix time) the maze began, which maze,
#and resets both cell and framecount. These data are stored
#as two values in movearray.
def timestampmazestamp(when, whichmaze):
    global movearray
    global cell
    global framecount
    cell = 0
    framecount = 10000
    when = str(when)
    timestampstringlength = len(when)
    if(timestampstringlength < 15):
        for x in range(0, (15 - timestampstringlength)):
            when = when + " "
    movearray.append(when)

    if((whichmaze < 10) and (whichmaze != -1)):
        whichmaze = str(whichmaze)
        whichmaze = "0" + whichmaze
    else:
        whichmaze = str(whichmaze)
    whichmaze = "Maze Number: " + whichmaze
    movearray.append(whichmaze)
    

#storemove stores test subjects' movements in movearray.
#movearray: when, where, how
def storemove(direction):
    global movearray
    global cell
    global framecount
    movearray.append((framecount, (cell+10000), direction))

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

    
#movecircle moves the circle. Takes integer input.
#0:right
#1:up
#2:left
#3:down
def movecircle(direction):
    global cell
    global mazerun_number
    if(mazerun_number == 5):
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
            
#pygame.key.get_focused() returns 1 if keyboard input is focussed on window
#pygame.key.get_focused() returns 0 if keyboard input is not focussed on window
#---==== TIME SYNC HERE ===---
#waits for keyboard focus to leave window (because user has clicked "start EEG
#recording" in Emotiv's software interface in a different window) and records
#a timestamp that notes when that happened
mazenumber = -1
while True:
    pygame.event.get()
    timestamp = time.time()
    if(pygame.key.get_focused() == 0):
        break
timestampmazestamp(timestamp, mazenumber)
while True:
    pygame.event.get()
    if(pygame.key.get_focused() == 1):
        break
#----==== MAIN LOOP HERE ===-----
while True:
    if(mazerun_number == 5):
        if(mazenumber == 29):
            pygame.quit()
            sys.exit()
        mazenumber = mazenumber + 1
        mazerun_number = -1



    mazerun_number = mazerun_number + 1
    openmaze(mazenumber)

    timestamp = time.time()
    if(mazerun_number == 5):
        timestampmazestamp(timestamp, mazenumber)
    while True: #maze running with event logging happens inside this loop.
        
        #quit cleanly. The user input event handler lives here too.
        for event in pygame.event.get():
            if(event.type == QUIT):
                pygame.quit()
                sys.exit()
            #user input event handler :D
            if(event.type == KEYDOWN):
                if(event.key == K_RIGHT):
                    movecircle(0)
                if(event.key == K_UP):
                    movecircle(1)
                if(event.key == K_LEFT):
                    movecircle(2)
                if(event.key == K_DOWN):
                    movecircle(3)


        #blit (copy) the maze image to the display surface.
        #in this case the top left corner is at 575 (a ways over), 25 (a little
        #bit down from the top because Y IS INVERTED)
        displaysurface.blit(mazeimage, (575,25))

        #convert from cell number to pixel location and store as circleposition
        circleposition = celltoposition(cell)
        #draw the circle in the maze.
        pygame.draw.circle(displaysurface, (0,255,255), circleposition, 20, 0)

        #update the whole display.
        pygame.display.update()

        #This goes at the VERY END of main loop!
        fpsClock.tick(FPS) #tick FPS clock
        framecount = framecount + 1 #increment framecount

        if(cell == 143):
            if(mazerun_number == 5):
                storemove(5) #because when you finish the maze, that's a 5.
            cell = 0
            break
