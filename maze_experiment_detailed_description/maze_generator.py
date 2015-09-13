#this program is a primitive 3x3 maze generator using recursive backtracking
#it will be updated to 10x10 once shown to work as 3x3. ::EDIT:: It lives! 3x3 and 4x4
#maze generating ability confirmed by hand-drawing array ouptut. Now to kludge the
#rendering engine into this code to get the rendering code done/tested/working.
#After that I'll have to split this all up gracefully and make data structures for it.

import random, pygame, sys, math
from pygame.locals import *

#init stuff for pygame
pygame.init()
FPS = 30
fpsClock = pygame.time.Clock()

#this dimension sets both the length and height of the maze
mazedimension = 12
#DO NOT FORGET Y IS INVERTED FOR THE FOLLOWING! TOP LEFT IS (0,0)
#this is where on the screen (x, y) the bottom left corner of the maze is
mazebottomleft = (10, 640)
#this is how big each cell of the maze is, in pixels
mazecell = 50

#location will be pushed to this stack, reaching -1 terminates algorithm
global locationstack
locationstack = [-1]
#maze data stored in this array
global mazearray
mazearray = []


#this function initializes the maze
def mazeinit():
    for x in range (0, (mazedimension * mazedimension)):
#first var: visited? 2nd var: right wall? 3rd var: upper wall?
                    mazearray.append((0,1,1))

#this function carves a random cell if possible, returning 1
#returning 0 means that carving was impossible
def randcarve():
    global currentcell
    global mazearray

    #initialize available carve variables (default yes, i.e. 1)
    rightvalid = 1
    upvalid = 1
    leftvalid = 1
    downvalid = 1

    #testing for edges!
    #are we on the bottom edge?
    if(currentcell < mazedimension):
        downvalid = 0
    #are we on the top edge?
    if(currentcell > ((mazedimension * mazedimension) - 1) - mazedimension):
        upvalid = 0
    #are we on the left edge?
    if((currentcell % mazedimension) == 0):
        leftvalid = 0
    #are we on the right edge?
    if((currentcell % mazedimension) == (mazedimension - 1)):
        rightvalid = 0

    #having checked for edges, now we must check for visitation status
    #right visited?
    if(currentcell != (mazedimension * mazedimension) - 1): #don't leave the array
        if(mazearray[currentcell + 1][0] == 1):
            rightvalid = 0

    #up visited?
    if(currentcell < (mazedimension * mazedimension) - mazedimension):
        if(mazearray[currentcell + mazedimension][0] == 1):
            upvalid = 0

    #left visited?
    if(currentcell != 0):
        if(mazearray[currentcell - 1][0] == 1):
            leftvalid = 0

    #down visited?
    if(currentcell > mazedimension - 1):
        if(mazearray[currentcell - mazedimension][0] == 1):
            downvalid = 0
        
    #this must be run after all carve checks
    if((downvalid == 0) and (upvalid == 0) and (leftvalid == 0) and (rightvalid == 0)):
        return 0

    #we did all the carve checks and returned 0 if we couldn't carve, so if we're here
    #it means we must be able to carve, so let's do that!

    while True: #this loop will generate a direction that's guaranteed to align with a valid carve
        
        #0=right, 1=up, 2=left, 3=down
        rightupleftdown = math.floor(random.random() * 4)
        
        if((rightupleftdown == 0) and (rightvalid == 1)):
            break
        if((rightupleftdown == 1) and (upvalid == 1)):
            break
        if((rightupleftdown == 2) and (leftvalid == 1)):
            break
        if((rightupleftdown == 3) and (downvalid == 1)):
            break

    #so now we know that rightupleftdown contains a valid carve direction, randomly chosen
    if(rightupleftdown == 0):
        mazearray[currentcell] = (mazearray[currentcell][0], 0, mazearray[currentcell][2])
        currentcell = currentcell + 1
    if(rightupleftdown == 1):
        mazearray[currentcell] = (mazearray[currentcell][0], mazearray[currentcell][1], 0)
        currentcell = currentcell + mazedimension
    if(rightupleftdown == 2):
        currentcell = currentcell - 1
        mazearray[currentcell] = (mazearray[currentcell][0], 0, mazearray[currentcell][2])
    if(rightupleftdown == 3):
        currentcell = currentcell - mazedimension
        mazearray[currentcell] = (mazearray[currentcell][0], mazearray[currentcell][1], 0)
    
    
    
#------====== MAZE GENERATOR STARTS =======-------

#initialize maze
mazeinit()
#select position in maze index
global currentcell
currentcell = math.floor(random.random() * (mazedimension * mazedimension))
mazedone = 0

#getting out of this while loop means that we have a complete maze array.
while(mazedone == 0):
    #push location on locationstack
    locationstack.append(currentcell) 
    #flag current cell as visited
    mazearray[currentcell] = (1, mazearray[currentcell][1], mazearray[currentcell][2])
    
    while(randcarve() == 0):
        currentcell = locationstack.pop()
        if(currentcell == -1):
            mazedone = 1
            break
#------======= MAZE GENERATOR ENDS =====--------
#NOTE: MAZEARRAY IS POPULATED NOW
#Just need to kludge some maze rendering code in here now...

#setting up the display window
DISPLAYSURF = pygame.display.set_mode((650, 650)) # could add more args for flags and depth
pygame.display.set_caption("MAZE!")

#------====== MAIN LOOP CONTAINING FPS TICKS======-------
while True:
    #clean quit code
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    #fps clock tick
    fpsClock.tick(FPS)
    #make the background black
    DISPLAYSURF.fill((0,0,0))
    #drawing lines for the border of the maze
    #draw the bottom!
    pygame.draw.line(DISPLAYSURF, (255,255,255), mazebottomleft,
                     ((mazebottomleft[0] + mazecell*mazedimension),mazebottomleft[1]),3)
    #draw the left.
    pygame.draw.line(DISPLAYSURF, (255,255,255), mazebottomleft,
                     (mazebottomleft[0], (mazebottomleft[1] - mazecell*mazedimension)),3)
    #draw the top!
    pygame.draw.line(DISPLAYSURF, (255,255,255),
                     (mazebottomleft[0],(mazebottomleft[1] - mazecell*mazedimension)),
                     (mazebottomleft[0] + mazecell*mazedimension,
                     (mazebottomleft[1] - mazecell*mazedimension)),3)
    #draw the right.
    pygame.draw.line(DISPLAYSURF, (255,255,255),
                     (mazebottomleft[0] + mazecell*mazedimension, mazebottomleft[1]),
                     (mazebottomleft[0] + mazecell*mazedimension,
                      mazebottomleft[1] - mazecell*mazedimension),3)
    #draw ALL THE LINES INSIDE!!
    for x in range (0, (mazedimension*mazedimension)):
        #let's make celltopright be the (x,y) of the cell's top right.
        #both drawn lines will start from celltopright.
        #ah, but where is celltopright? xval will be influenced by x % mazedimension, and
        #yval will be influenced by math.floor(x / mazedimension).
        celltopright = (mazebottomleft[0] + mazecell*(1 + (x % mazedimension)),
                        mazebottomleft[1] - mazecell*(1 + math.floor(x / mazedimension)))
        if(mazearray[x][1] == 1): #if there's a right wall...
            #draw the right wall
            pygame.draw.line(DISPLAYSURF, (255,255,255), celltopright,
                             (celltopright[0], celltopright[1] + mazecell),3)
                             
        if(mazearray[x][2] == 1): #if there's an upper wall...
            #draw the upper wall
            pygame.draw.line(DISPLAYSURF, (255,255,255), celltopright,
                             (celltopright[0] - mazecell,celltopright[1]),3)
        
    #update the whole display
    pygame.display.update()


