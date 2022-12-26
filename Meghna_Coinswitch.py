#################################################
# 00tp.py
# Your name: Meghna Koushik
# Your andrew id: meghnak
#################################################


from multiprocessing.sharedctypes import Value
from textwrap import fill
from turtle import tiltangle, width
from typing import ValuesView
import random
import math, copy, os
from xmlrpc.client import FastMarshaller
from black import color_diff
from cmu_112_graphics import *
import io
import requests
from PIL import Image
import os
import pygame


#A version of the class Notes from Strings
#Function to read file
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

#Function to write file
def writeFile(path, contents):
    with open(path, "a") as f:
        f.writelines(contents)


#From TA, Kian's notes: Piazza post
class Sound(object):
    currentChannel = 0 
    #The default max is 8 channels

    def __init__(self, path):
        self.path = path
        self.loops = 0
        self.channel = Sound.currentChannel
        Sound.currentChannel += 1 
        #Ensures the next Sound is on a different channel

    def start(self, loops=0):
        self.loops = loops
        pygame.mixer.Channel(self.channel).play(pygame.mixer.Sound(self.path), loops=loops)

    def stop(self):
        pygame.mixer.Channel(self.channel).stop(pygame.mixer.Sound(self))

##########################################
# LeaderBoard Mode
##########################################

def leaderboardMode_redrawAll(app, canvas):
    #creating a background
    #Background for instruction mode: Original Artwork
    canvas.create_image(app.width, app.height,
    image=ImageTk.PhotoImage(app.background2))
    canvas.create_image(app.width/2, app.height*1/7,
    image=ImageTk.PhotoImage(app.logo))

    count = -1
    #Loop to write the LeaderBoard
    for index in range(len(app.lines)):
        #Allow only 10 entries on the leaderboard
        if index < 10:
            key = app.lines[index]
            name = key[0]
            score = key[1]
            count += 1
            dy = 50
            canvas.create_text( app.width/4, 200 + count*dy,
            fill= "White", text= name, 
            font=f'Arial 20 bold', anchor = 'n')
            canvas.create_text( app.width*3/4,200 + count*dy,
            fill= "White", text= score, 
            font=f'Arial 20 bold', anchor = 'n')

#Return to MainScreen   
def leaderboardMode_keyPressed(app, event):
    if event.key == "r" or event.key == "R":
        appStarted(app)       

##########################################
# Instruction Mode
##########################################

def instructionMode_redrawAll(app, canvas):
    #creating a background
        #Background for instruction mode: Original Artwork
        canvas.create_image(app.width, app.height,
        image=ImageTk.PhotoImage(app.background2))
        canvas.create_image(app.width/2, app.height*1/7,
        image=ImageTk.PhotoImage(app.logo))

        #Text for instruction
        Instructiontext = '''    
                                Welcome to Coinswitch! The red and blue coins 
                                keep rotating alternately, hit space bar when the rotating 
                                coin is just about to land or has landed on a cell. 
                                Keep making your way through the path 
                                until you reach the end. If you miss, you lose. 
                                For Medium and Hard Modes, find your way through the maze.
                                Watch out for some "special tiles" in the medium and hard
                                levels. 
                
                                Press r to go back anyhwere in the game to 
                                go back to the Main Menu!'''

        canvas.create_text( app.width/2 - app.width/12 , app.height*7/24,
        fill= "White", text= Instructiontext, 
        font=f'Arial 15 bold', anchor = 'n')

#To go back to the main menu
def instructionMode_keyPressed(app, event):
    if event.key == "r" or event.key == "R":
        appStarted(app)


##########################################
# Splash Screen Mode
##########################################

def splashScreenMode_redrawAll(app, canvas):
    #creating a background: Original Artwork
        canvas.create_image(app.width, app.height,
        image=ImageTk.PhotoImage(app.background2))
        canvas.create_image(app.width/2, app.height*1/7,
        image=ImageTk.PhotoImage(app.logo))

        #Title text
        canvas.create_text( app.width/2 - 5, app.height/4,
        fill= "white", text= "Welcome to Coinswitch!", 
        font=f'Arial 45 bold')
        
        canvas.create_text( app.width/2, app.height/4,
        fill= "black", text= "Welcome to Coinswitch!", 
        font=f'Arial 45 bold')

        #drawing all modes, and text
        drawKey(app,canvas, app.width*1/4, app.height/2)
        drawKey(app,canvas, app.width*1/2, app.height/2)
        drawKey(app,canvas, app.width*3/4, app.height/2)
        drawKey(app,canvas, app.width*3/8, app.height*2/3)
        drawKey(app,canvas, app.width*5/8, app.height*2/3)
        createText(app, canvas, app.width*1/4, 
        (app.height/2 - app.SplashScreen_cellheight/2), "Easy Mode")
        createText(app, canvas, app.width*2/4, 
        (app.height/2 - app.SplashScreen_cellheight/2), "Medium Mode")
        createText(app, canvas, app.width*3/4, 
        (app.height/2 - app.SplashScreen_cellheight/2), "Hard Mode")
        createText(app, canvas, app.width*3/8, 
        (app.height*2/3 - app.SplashScreen_cellheight/2), "Instructions")
        createText(app, canvas, app.width*5/8, 
        (app.height*2/3 - app.SplashScreen_cellheight/2), "Leaderboard")
        
        canvas.create_text(app.width/2,  app.height/3,
                       text=app.message, font='Arial 15 bold', fill='black')

#Splashscreen Mousepressed:To check which mode to enter
def splashScreenMode_mousePressed(app, event):  
    (x, y) = (event.x , event.y)

    #From class notes
    if(app.width/4 - app.SplashScreen_cellwidth)  < event.x < (
    app.width/4 + app.SplashScreen_cellwidth):
        if (app.height/2 - app.SplashScreen_cellheight) < event.y < app.height/2:
            app.mode = 'easymode'
            
    elif (app.width/2 - app.SplashScreen_cellwidth) < event.x < (
        app.width/2 + app.SplashScreen_cellwidth):
        if (app.height/2 - app.SplashScreen_cellheight) < event.y < app.height/2:
            app.mode = 'mediumMode'

    elif (app.width*3/4 - app.SplashScreen_cellwidth) < event.x < (
        app.width*3/4 + app.SplashScreen_cellwidth):
        if (app.height/2 - app.SplashScreen_cellheight) < event.y < app.height/2:
            app.mode = 'hardMode'
    
    elif (app.width*3/8 - app.SplashScreen_cellwidth) < event.x < (
        app.width*3/8 + app.SplashScreen_cellwidth):
        if (app.height*2/3 - app.SplashScreen_cellheight) < event.y < (
            app.height*2/3):
            app.mode = 'instructionMode'

    elif (app.width*5/8 - app.SplashScreen_cellwidth) < event.x < (
        app.width*5/8 + app.SplashScreen_cellwidth):
        if (app.height*2/3 - app.SplashScreen_cellheight) < event.y < (
            app.height*2/3):
            app.mode = 'leaderboardMode'
    
    else:
        #From Class Notes
        name = app.getUserInput('What is your name?')
        if (name == None):
            app.message = 'You canceled!'
        else:
            app.message = f'Hi, {name}!' 
            app.name += name
    
    #Checking mode
    if (app.mode == 'easymode') or (app.mode == 'mediumMode') or (app.mode
        == 'hardMode'):
        appInit(app,app.mode)

#Helper functions to draw keys and add text
def drawKey(app, canvas, x, y):
    (x0, y0) = (x - app.SplashScreen_cellwidth, y)
    (x2, y2) = (x + app.SplashScreen_cellwidth, y0 - app.SplashScreen_cellheight) 
    canvas.create_rectangle(x0, y0, x2, y2,
                    fill = 'black',
                    outline = 'white',
                    width = 1.2)

def createText(app, canvas, x, y, modename):
    canvas.create_text(x, y, fill= "white",
                           text= modename, font=f'Arial 15 bold')


##########################################
# Main App
##########################################

###
#Model
###

def appStarted(app):
    #Mode
    app.text = readFile('Leaderboard.txt')
    app.lines = maketextDictionary(app, app.text)  
    app.name = ''

    #All images used: All Original artwork
    app.flashImage = app.loadImage('flash.png')
    app.slowImage = app.loadImage('slow.png')
    app.reverseImage = app.loadImage('reverse.png')
    app.background = app.loadImage('background.png')
    app.logo = app.loadImage('logo.png')

    #Input for name
    app.message = 'Click the mouse to enter your name!'

    #Common to all modes
    app.background2 = app.scaleImage(app.background, 2)
    app.StartingPoint = (app.width *1/2, app.width*1/2)
    app.gameOver = False
    app.Size =  30
    app.Height = 20
    app.rows = 21
    app.cols = 21
    app.endingPoint = (app.rows-1, app.cols-1) 
    app.rotationCount = 0
    app.gameOver = False
    app.ScrollX = 0 
    app.ScrollY = 0
    app.win = False
    app.color = True
    app.StartGrid = (0, 0)
    app.currRow = 0
    app.currCol = 0
    app.circlePosition = 0
    app.tiles = []
    app.hardModetiles = []
    app.nodes = []
    app.connectors = []
    app.timeStarted = 0
    app.timeElapsed = 0
    app.timeCheck = 100

    #Sound, from class notes
    pygame.mixer.init()

    #jump sound from Cabled_mess on freesound.org
    app.sound = Sound("jump.wav")
    #game die from jofae on freesound.org
    app.DeathSound = Sound("death.mp3")  
    #Action 03 from rhodesmas on freesound.org
    app.VictorySound = Sound("victory.wav")

    #All types of tiles
    app.specialTiles = []
    app.fast = []
    app.slow = []
    app.reverse = []
    app.sideMoving = []
    app.sideMovingCount = 0
    app.sideMovingList = [(-1, 0), (+1, 0), (+1, 0), (-1, 0)]
    app.topMoving = []
    app.colorChangingList = []
    app.colorChanging = [rgbString(71, 196, 218), rgbString(202, 78, 44)]
    app.colorCount = True

    #SplashscreenMode
    app.mode = 'splashScreenMode'
    app.SplashScreen_cellwidth = 80
    app.SplashScreen_cellheight = 40  
    app.rotationTally = 0

    #for easymode path generation
    app.startingPointList = []
    app.startingPointList.append((app.currRow, app.currCol))
    easymode_getPath(app, app.currRow, app.currCol)
    (x, y) = app.startingPointList[1]
    app.currentNeighbors = getRotationalPath(app, x, y)

#Helper function to add specific functions for specific modes
def appInit(app, mode):
    #medium Mode
    if mode == "mediumMode":
        mediumMode_getgrid(app)
        mediumMode_getMaze(app)
        mediumMode_deleteRandomTiles(app)
        pickRandomTiles(app)
        (x, y) = (0, 1)
        app.currentNeighbors = getRotationalPath(app, x, y)

    #HardMode
    elif mode == "hardMode":
        hardMode_getgrid(app)
        hardMode_getMaze(app)
        hardMode_pickrandomtiles(app)
        (x, y) = (0, 1)
        app.currentNeighbors = getRotationalPath(app, x, y)

    #EasyMode
    if mode == "easyMode":
        (x, y) = app.startingPointList[1]
        app.currentNeighbors = getRotationalPath(app, x, y)
    app.timerDelay = 25

#From class Notes- Helper function to get color
def rgbString(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

#Helper function: to read 
def maketextDictionary(app, text):
    result  = []
    for lines in text.splitlines():
        (name, score) = lines.split(":")
        result = result + [[name, int(score)]]
    result = sorted(result,key=lambda l:l[1], reverse=True)
    return result

#A version of wordSearch logic from notes  
def getRotationalPath(app, row, col):
    if app.gameOver == False:
        result = []
        neighbors = [(+1, 0), (+1, +1), (0, +1), (-1, +1),
                    (-1, 0), (-1, -1), (0, -1), (+1, -1)]
        for dir in neighbors:
            (x, y) = dir
            result.append((row + x, col + y))
        return result   
    return None  

#A version of wordSearch logic to get reverse path
def getReverseRotationalPath(app, row, col):
    if app.gameOver == False:
        result = []
        neighbors = [(+1, 0), (+1, +1), (0, +1), (-1, +1),
                    (-1, 0), (-1, -1), (0, -1), (+1, -1)]
        for index in range(len(neighbors)-1, -1, -1):
            (x, y) = neighbors[index]
            result.append((row + x, col + y))
        return result   
    return None   

#Helper function to get starting point from a given cell row & col
def getStartingPoint(app, row, col):
    (x, y) = app.StartingPoint 
    x0 = x + row * app.Size + col * app.Size
    y0 = y + row * app.Size - col * app.Size
    return (x0 , y0)

#Checking legality of newly genrated rows and cols
def isLegal(app, newRow, newCol):
    if  app.rows > newRow >= 0 and app.cols > newCol >= 0:
                if (newRow , newCol) not in app.startingPointList:
                    if hasNeighbor(app, newRow, newCol) == False:
                        return True
    return False


#A version of wordSearch logic from notes        
def hasNeighbor(app, newRow, newCol):
    diagonalDirections = [(-1, -1), (-1, +1), (+1, -1),  (+1, +1)]
    directional = [(-1, 0),(0, -1), (0, +1), (+1, 0)]
    countDiagonal = 0
    countDirectional = 0

    #looping over diagonal search
    for direction in diagonalDirections:
        (dx, dy) = direction
        (refRow , refCol) = (newRow + dx, newCol +  dy)
        if (refRow, refCol) in app.startingPointList:
            countDiagonal += 1

    #looping over directinal neighbors
    for direction2 in directional:
        (dx, dy) = direction2
        (refRow , refCol) = (newRow + dx, newCol +  dy)
        if (refRow, refCol) in app.startingPointList:
            countDirectional += 1

    #Allowing only 1 diagonal and 1 dimensional
    if countDiagonal > 2 or countDirectional > 1:
        return True
    return False

#Helper Function to draw Tile                
def drawTile(app, canvas, x, y):
    (x0, y0) = (x, y)
    (x1, y1) = (x0 - app.Size, y0 - app.Size)
    (x2, y2) = (x0 , y0 - 2*app.Size) 
    (x3, y3) = (x0 + app.Size, y0 - app.Size)
    canvas.create_polygon(x0, y0, x1, y1,
                    x2, y2, x3, y3,
                    fill = 'black',
                    outline = 'white',
                    width = 1.2) 

#Helper Function to draw Special Tiles  
def drawColorTile(app, canvas, x, y, color):
    (x0, y0) = (x, y)
    (x1, y1) = (x0 - app.Size, y0 - app.Size)
    (x2, y2) = (x0 , y0 - 2*app.Size) 
    (x3, y3) = (x0 + app.Size, y0 - app.Size)
    canvas.create_polygon(x0, y0, x1, y1,
                    x2, y2, x3, y3,
                    fill = color,
                    outline = 'white',
                    width = 1.2) 

#Helper funtion: To draw image over Special tile flash/ fast
def drawFlash(app, canvas, x, y):  
    (x0, y0) = (x, y)
    (x1, y1) = (x0 - app.Size, y0 - app.Size)
    (x2, y2) = (x0 , y0 - 2*app.Size) 
    (x3, y3) = (x0 + app.Size, y0 - app.Size) 
    canvas.create_image((x1+x3)/2, (y1+y3)/2, 
    image=ImageTk.PhotoImage(app.flashImage))

#Helper funtion: To draw image over Special tile slow
def drawSlow(app, canvas, x, y):  
    (x0, y0) = (x, y)
    (x1, y1) = (x0 - app.Size, y0 - app.Size)
    (x2, y2) = (x0 , y0 - 2*app.Size) 
    (x3, y3) = (x0 + app.Size, y0 - app.Size) 
    canvas.create_image((x1+x3)/2, (y1+y3)/2, 
    image=ImageTk.PhotoImage(app.slowImage))

#Helper function: To draw reverse
def drawReverse(app, canvas, x, y):  
    (x0, y0) = (x, y)
    (x1, y1) = (x0 - app.Size, y0 - app.Size)
    (x2, y2) = (x0 , y0 - 2*app.Size) 
    (x3, y3) = (x0 + app.Size, y0 - app.Size) 
    canvas.create_image((x1+x3)/2, (y1+y3)/2, 
    image=ImageTk.PhotoImage(app.reverseImage))

#Helper Function: to draw height for the tile
def drawHeightLeft(app, canvas, x, y):
    (x0, y0) = (x, y)
    (x1, y1) = (x0 - app.Size, y0 - app.Size)
    canvas.create_polygon(x0, y0, x0, y0 + app.Height,
                          x1, y1 + app.Height, x1, y1,
                          fill = rgbString(252, 176, 92))


#Helper Function: to draw height for the tile
def drawHeightRight(app, canvas, x, y):
    (x0, y0) = (x, y)
    (x3, y3) = (x0 + app.Size, y0 - app.Size)
    canvas.create_polygon(x0, y0, x0, y0 + app.Height,
                          x3, y3 + app.Height, x3, y3,
                          fill = rgbString(242, 103, 98))


#Helper Function: to draw the circle 1
def drawCircle1(app, canvas, x, y):
    (x0, y0) = (x, y)
    (x1, y1) = (x0 - app.Size, y0 - app.Size)
    (x2, y2) = (x0 , y0 - 2*app.Size) 
    (x3, y3) = (x0 + app.Size, y0 - app.Size)
    (x4, y4) = ((x0 + x1) / 2 , (y0 + y1) / 2 )
    (x5, y5) = ((x2 + x3) / 2 , (y2 + y3) / 2 )
    canvas.create_oval(x4, y4, x5, y5,
                          fill = rgbString(71, 196, 218),
                          outline = "white")


#Helper Function: to draw the circle 2
def drawCircle2(app, canvas, x, y):
    (x0, y0) = (x, y)
    (x1, y1) = (x0 - app.Size, y0 - app.Size)
    (x2, y2) = (x0 , y0 - 2*app.Size) 
    (x3, y3) = (x0 + app.Size, y0 - app.Size)
    (x4, y4) = ((x0 + x1) / 2 , (y0 + y1) / 2 )
    (x5, y5) = ((x2 + x3) / 2 , (y2 + y3) / 2 )
    canvas.create_oval(x4, y4, x5, y5,
                          fill = rgbString(202, 78, 44),
                          outline = "white")

##########################################
#   Easy Mode
##########################################

def easymode_timerFired(app):
    #Keeping track of time elapsed
    app.timeElapsed += app.timerDelay

    #Checking for win and Game over
    if app.win == False:
        if app.gameOver == False:
            #incrementing and looping over rotation count of circles
            if app.timeElapsed % app.timeCheck == 0:
                app.rotationCount += 1
                if app.rotationCount > 7:
                    app.rotationCount = 0
        else:
            app.gameOver = True

def easymode_keyPressed(app, event): 
    if app.gameOver == False:
        if event.key == "Space":
            rotationCountTemp = app.rotationCount
            #Checking if the circle position is in the path list
            if app.currentNeighbors[rotationCountTemp] in app.startingPointList:
                #Start Sound evertime space is hit correctly
                #app.sound.start()
                #if yes, generating co-ordinates for it and updating the row 
                #col for circle position
                (x1, y1) = app.startingPointList[app.circlePosition + 1]
                value = app.startingPointList.index(app.currentNeighbors[rotationCountTemp])
                app.circlePosition = value - 1 
                (x, y) = app.startingPointList[app.circlePosition + 1] 

                #checking if the circle has reached the endpoint
                if (x, y) == app.endingPoint:
                    app.gameOver = True
                    app.win = True
                    #app.VictorySound.start()
                    Name = str(app.name)
                    Score = str(app.circlePosition)
                    writeFile('Leaderboard.txt', Name + ':' + Score + '\n')
                    app.currentNeighbors = []
                #if not, generate new neighbors for circle rotation   
                app.currentNeighbors = getRotationalPath(app, x, y)

                #Color toggle for the circles
                if app.color == False:
                    app.color = True
                else:
                    app.color = False

                #factoring side scrolling
                if (y - y1) > 0:
                    app.ScrollX += 40
                    app.ScrollY -= 40
                elif (y - y1) < 0:
                    app.ScrollX -= 40
                    app.ScrollY += 40
                elif (x - x1) > 0:
                    app.ScrollX += 40
                    app.ScrollY += 40
                elif (x - x1) < 0:
                    app.ScrollX -= 40
                    app.ScrollY -= 40

            #Else: it's in the wrong place, game over! 
            else: 
               app.gameOver = True
               #app.DeathSound.start()
               Name = str(app.name)
               Score = str(app.circlePosition)
               writeFile('Leaderboard.txt', Name + ':' + Score +'\n')
               app.win = False

    #other event keys to resent
    if event.key == "r" or event.key == "R":
        appStarted(app)          

#Path generation: Easy mode
def easymode_getPath(app, row, col):
    #Base case
    if (row, col) == app.endingPoint:
        return app.startingPointList

    #Recursive Case
    else:
        possibleDirections = [(-1, 0), (0, +1), (+1, 0)]
        shuffled = possibleDirections
        #iterating over random order of possible directions
        random.shuffle(shuffled)
        for value in shuffled:
            (dx, dy) = value
            (newRow , newCol) = (row + dx, col +  dy)
            if isLegal(app, newRow, newCol) == True:
                app.startingPointList.append((newRow, newCol))
                result = easymode_getPath(app, newRow, newCol)
                if result != None:
                    return result

                #if result cannot be done, backtrack
                else: 
                    app.startingPointList.remove((newRow, newCol))
    return None

###
#View
###

def easymode_redrawAll(app, canvas):
    if app.gameOver == False: 
        #creating a background
        canvas.create_image(app.width, app.height,
         image=ImageTk.PhotoImage(app.background2))
        canvas.create_text(100, 50, fill= "black",
                           text=  f'Score: {app.circlePosition}', 
                           font=f'Arial 20 bold') 

        #drawing heights of for all points in path list
        for index in range(len(app.startingPointList)):
            (x, y) = app.startingPointList[index]
            (x1, y1)= getStartingPoint(app, x, y)
            (x1, y1)= (x1-app.ScrollX, y1-app.ScrollY)
            #check to draw heights only if required
            if (x+1, y) not in app.startingPointList:
                drawHeightRight(app, canvas, x1, y1)
            if (x, y-1) not in app.startingPointList:
                drawHeightLeft(app, canvas, x1, y1)

        #drawing tiles for all points
        for index2 in range(len(app.startingPointList)):
            (x, y) = app.startingPointList[index2]
            (x1, y1)= getStartingPoint(app, x, y)
            (x1, y1)= (x1-app.ScrollX, y1-app.ScrollY)
            drawTile(app,canvas, x1, y1) 

        #drawing circles2 and 1
        if app.circlePosition < len(app.startingPointList)-1:
                (row, col) = app.currentNeighbors[app.rotationCount]
                (x, y) = getStartingPoint(app, row, col)
                (x, y)= (x-app.ScrollX, y-app.ScrollY)

                #drawing intial circles
                if app.circlePosition == 0 and (0, 2) in app.currentNeighbors:
                    (x2, y2) = (0, 1)
                    (x3, y3)= getStartingPoint(app, x2, y2)
                    (x3, y3)= (x3-app.ScrollX, y3-app.ScrollY)

                elif app.circlePosition == 0 and (2, 0) in app.currentNeighbors:
                    (x2, y2) = (1, 0)
                    (x3, y3)= getStartingPoint(app, x2, y2)
                    (x3, y3)= (x3-app.ScrollX, y3-app.ScrollY)

                #drawing all subsequent circles
                else:
                    (x2, y2) = app.startingPointList[app.circlePosition + 1]
                    (x3, y3)= getStartingPoint(app, x2, y2)
                    (x3, y3)= (x3-app.ScrollX, y3-app.ScrollY)

                #checking toggle and drawing appropriate circle
                if app.color == True:
                    drawCircle1(app, canvas, x, y)
                    drawCircle2(app, canvas, x3, y3)

                else:
                    drawCircle2(app, canvas, x, y)
                    drawCircle1(app, canvas, x3, y3)

    #if the player has won, creating win text!
    else:
        if  app.win == True:
            canvas.create_rectangle(0,0,app.width, app.height, fill= "black")
            canvas.create_text(app.width/2, app.height/2, fill= "white",
                           text= "You have won!", font= f'Arial 30 bold')
        else:
            canvas.create_rectangle(0,0,app.width, app.height, fill= "black")
            canvas.create_text(app.width/2, app.height/2, fill= "white",
                           text= "Game Over, Press R to restart", 
                           font=f'Arial 30 bold')   
                        
##########################################
#  Medium Mode
##########################################

#Helper function to pick random tiles for special tiles
def pickRandomTiles(app):
    for index in range(int(len(app.tiles)//5)):
        randomNum = app.tiles[random.randint(0, len(app.tiles)-1)]
        if randomNum not in app.fast and randomNum not in app.slow:
            if index % 2 == 0:
                app.fast.append(randomNum)
            else: 
                app.slow.append(randomNum)

#Deleting random tiles that don't add to the path from Kruskal's maze generation
def mediumMode_deleteRandomTiles(app):
    necessaryList = [(0, 0),(0, 1),(0, 2),(0, 3)]
    for index in range(int(len(app.tiles)//3)):
        randomNum = app.tiles[random.randint(0, len(app.tiles)-1)]
        mediumDict = mediumMode_getDict(app)
        if randomNum not in necessaryList:
            app.tiles.remove(randomNum)
        if areConnected(app, app.StartGrid, app.endingPoint, mediumDict) == False:
            app.tiles.append(randomNum)

#helper function: to create a new dictionary
def mediumMode_getDict(app):
    result = dict()
    for t1 in app.nodes:
        result[t1] = result.get(t1, 0)
    for t2 in app.connectors:
        result[t2] = result.get(t2, 0)
    return result

#helper function: to get grid
def mediumMode_getgrid(app):
    result = []
    for row in range(app.rows):
        for col in range(app.cols):
            result.append((row, col))
            if row % 2 == 0 and col % 2 == 0:
                app.nodes.append((row, col))
            else:
                app.connectors.append((row, col))
    return result

#Helper function: Picking random node neighbor (Kruskal's)
def mediumMode_pickRandomnodeNeighbor(app, r, c):
    neighbors = [(-2, 0),(0, -2), (0, +2), (+2, 0)]
    random.shuffle(neighbors)
    for n in neighbors:
        (dx, dy) = n
        (row, col) = (r + dx, c + dy)
        if 0 <= row < app.rows and 0 <= col < app.cols:
            return (row, col)
    return None

#Helper function: Random Tile Generator
def randomTileGenerator(app):
    r = random.randint(0, app.rows - 1)
    c = random.randint(0, app.cols - 1)
    return (r, c)

#DFS: Depth First Search
#To checkif two nodes in a grid are connected
def areConnected(app, start, end, mediumDict):
    neighbors = [(-1, 0),(0, -1), (0, +1), (+1, 0)]
    #Base case
    if start == end:
        return True
    
    else:
        #for move in moves
        for value in neighbors:
            mediumDict[start] = 1
            (dx, dy) = value
            (x, y) = start
            (row, col) = (x+ dx, y+ dy)
            #check if legal
            if 0 <= row < app.rows and 0 <= col < app.cols:
                if (row, col) in app.tiles:
                    current = (row, col)
                    if mediumDict[current] == 0:
                    #if result is in solved state
                        result = areConnected(app, current, end, mediumDict)
                    #if not false return result
                        if result != False:
                            return result 
                        else:
                            current = start   
            mediumDict[start] = 0 
    return False             
                    
#Kruskal's Algorhithm for Maze generation
def mediumMode_getMaze(app):
    reqNodes = app.nodes
    random.shuffle(reqNodes)
    app.tiles.append((0, 1))
    app.tiles.append((0, 2))
    app.tiles.append((0, 3))
    mediumDict = mediumMode_getDict(app)
    NeighborDict = dict ()
    
    #while starting and ending points are not connected 
    is_loop=areConnected(app, app.StartGrid, app.endingPoint, mediumDict)
    while is_loop == False:
        #for a random ordered node in list of nodes
        for nodes in reqNodes:
            NeighborDict[nodes] = NeighborDict.get(nodes, [])
            if nodes not in app.tiles:
                app.tiles.append(nodes)
            (row, col) = nodes
            #pick random node neighbor
            n = mediumMode_pickRandomnodeNeighbor(app, row, col)
            if n  not in NeighborDict[nodes]:
                NeighborDict[nodes].append(n)
                if n not in app.tiles:
                    app.tiles.append(n)
                (r, c) = n
                #if they're not connected
                mediumDict = mediumMode_getDict(app)
                if areConnected (app, nodes, n, mediumDict) == False:
                    edge = (int((row + r)/2), int((col+c)/2))
                    (row1, col1) = edge
                #connect them
                    if 0 <= row1 < app.rows or 0 <= col1 < app.cols:
                        app.tiles.append(edge)
                #else: do nothing
        mediumDict = mediumMode_getDict(app)
        is_loop=areConnected(app, app.StartGrid, app.endingPoint, mediumDict) 
    return app.tiles.sort()

def mediumMode_timerFired(app):
    #checking time elapsed and incrementing circle rotation count
    app.timeElapsed += app.timerDelay
    if app.win == False:
        if app.gameOver == False:
            if app.timeElapsed % app.timeCheck == 0:
                app.rotationCount += 1
                if app.rotationCount > 7:
                    app.rotationCount = 0

    
def mediumMode_keyPressed(app, event): 
    if app.gameOver == False:
        if event.key == "Space":
            #if the circle's current position is on any of the tiles
            rotationCountTemp = app.rotationCount
            if app.currentNeighbors[rotationCountTemp] in app.tiles:
                #jump sound if correct jump
                #app.sound.start()
                (x1, y1) = app.tiles[app.circlePosition + 1]
                value = app.tiles.index(app.currentNeighbors[rotationCountTemp])
                app.circlePosition = value - 1 
                (x, y) = app.tiles[app.circlePosition + 1] 

                #checking for "special tiles"
                if (x, y) in app.fast:
                    app.timeCheck = 75
                elif (x, y) in app.slow:
                    app.timeCheck = 300
                else: 
                    app.timeCheck = 150

                #if ending point is reached, declare victory
                if (x, y) == app.endingPoint:
                    app.gameOver = True
                    app.VictorySound.start()
                    app.win = True
                    app.currentNeighbors = []
                
                #if not, get neighbors for current position
                app.currentNeighbors = getRotationalPath(app, x, y)

                #checking for the color of the circle
                if app.color == False:
                    app.color = True
                else:
                    app.color = False

                #factoring for side scrolling
                if (y - y1) > 0:
                    app.ScrollX += 25
                    app.ScrollY -= 25
                elif (y - y1) < 0:
                    app.ScrollX -= 25
                    app.ScrollY += 25
                elif (x - x1) > 0:
                    app.ScrollX += 25
                    app.ScrollY += 25
                elif (x - x1) < 0:
                    app.ScrollX -= 25
                    app.ScrollY -= 25
            
            #if circle position not in tiles, it's in wrong place
            else:
               app.gameOver = True 
               app.win = False
               #app.DeathSound.start() 
    
    #if key r is presssed,  reset
    if event.key == "r" or event.key == "R":
        appStarted(app) 

            
def mediumMode_redrawAll(app, canvas):
    #creating a background
    canvas.create_image(app.width, app.height,
    image=ImageTk.PhotoImage(app.background2))

    if app.gameOver == False:
        #drawing all heights
        for index in range(len(app.tiles)):
            (x, y) = app.tiles[index]
            (x1, y1)= getStartingPoint(app, x, y)
            (x1, y1)= (x1-app.ScrollX, y1-app.ScrollY)

            if (x+1, y) not in app.tiles:
                drawHeightRight(app, canvas, x1, y1)

            if (x, y-1) not in app.tiles:
                drawHeightLeft(app, canvas, x1, y1)

        #drawing tiles for all points
        for index2 in range(len(app.tiles)):
            (x, y) = app.tiles[index2]
            (x1, y1)= getStartingPoint(app, x, y)
            (x1, y1)= (x1-app.ScrollX, y1-app.ScrollY)
            drawTile(app,canvas, x1, y1) 

        #checking for fast tile, and drawing the fast vector
        for item in range(len(app.fast)):
            (x, y) = app.fast[item]
            (x1, y1)= getStartingPoint(app, x, y)
            (x1, y1)= (x1-app.ScrollX, y1-app.ScrollY)
            drawFlash(app, canvas, x1, y1)

        #checking for slow tikes,and drawing the slow vector
        for item2 in range(len(app.slow)):
            (x, y) = app.slow[item2]
            (x1, y1)= getStartingPoint(app, x, y)
            (x1, y1)= (x1-app.ScrollX, y1-app.ScrollY)
            drawSlow(app, canvas, x1, y1)

        #drawing circles2 and 1
        if app.circlePosition < len(app.tiles)-1:
                (row, col) = app.currentNeighbors[app.rotationCount]
                (x, y) = getStartingPoint(app, row, col)
                (x, y)= (x-app.ScrollX, y-app.ScrollY)
                (x2, y2) = app.tiles[app.circlePosition + 1]
                (x3, y3)= getStartingPoint(app, x2, y2)
                (x3, y3)= (x3-app.ScrollX, y3-app.ScrollY)
                
                #Checking color toggle and drawing appropriate circle
                if app.color == True:
                    drawCircle1(app, canvas, x, y)
                    drawCircle2(app, canvas, x3, y3)

                else:
                    drawCircle2(app, canvas, x, y)
                    drawCircle1(app, canvas, x3, y3)
    
    #if game over or the player has won, show text
    else:
        if  app.win == True:
            canvas.create_rectangle(0,0,app.width, app.height, fill= "black")
            canvas.create_text(app.width/2, app.height/2, fill= "black",
                           text= "You have won!", font= f'Arial 30 bold', outline = "white",
                           width = 10)
        else:
            canvas.create_rectangle(0,0,app.width, app.height, fill= "black")
            canvas.create_text(app.width/2, app.height/2, fill= "White",
                           text= "Game Over, Press R to restart", font=f'Arial 30 bold')

##########################################
#Hard Mode
##########################################

#Helper function: to create a trajectory for side moving tiles
def sidemoveTrajectory(app, x, y):
    result = [(x-1, y), (x, y), (x+1, y)]
    return result

#Helper function: To pick special tiles
def hardMode_pickrandomtiles(app):
    for index in range(len(app.tiles)//3):
        randomNum = app.tiles[random.randint(0, len(app.tiles)-1)]
        if randomNum not in app.specialTiles:
            #Assigning random tikes as special tiles
            if index % 4 == 0:
                app.fast.append(randomNum)
                app.specialTiles.append(randomNum)
            elif index % 6 == 0:
                app.slow.append(randomNum)
                app.specialTiles.append(randomNum)
            elif index % 7 == 0:
                app.reverse.append(randomNum)
                app.specialTiles.append(randomNum)

            else:
                #Adding moving tiles
                if index % 2 == 0 and len(app.sideMoving) < 3:
                    app.sideMoving.append(index)
                    app.specialTiles.append(randomNum)
                
                #Add color tiles
                elif index % 2 != 0 and len(app.colorChangingList) < 3:
                    app.colorChangingList.append(randomNum)
                    app.specialTiles.append(randomNum)

#To create a new dictionary
def hardMode_getDict(app):
    result = dict()
    for t1 in app.nodes:
        result[t1] = result.get(t1, 0)
    for t2 in app.connectors:
        result[t2] = result.get(t2, 0)
    return result

#to get grid from the current rows and cols
def hardMode_getgrid(app):
    result = []
    for row in range(app.rows):
        for col in range(app.cols):
            result.append((row, col))
            if row % 2 == 0 and col % 2 == 0:
                app.nodes.append((row, col))
            else:
                app.connectors.append((row, col))
    return result

#Helper Function: To pick random node neighbir (For Kruskals)
def hardMode_pickRandomnodeNeighbor(app, r, c):
    neighbors = [(-2, 0),(0, -2), (0, +2), (+2, 0)]
    random.shuffle(neighbors)
    for n in neighbors:
        (dx, dy) = n
        (row, col) = (r + dx, c + dy)
        if 0 <= row < app.rows and 0 <= col < app.cols:
            return (row, col)
    return None         
                    
#Hard Mode- Kruskal's Algorithm for maze generation
def hardMode_getMaze(app):
    reqNodes = app.nodes
    random.shuffle(reqNodes)
    app.tiles.append((0, 1))
    app.tiles.append((0, 2))
    app.tiles.append((0, 3))
    mediumDict = mediumMode_getDict(app)
    NeighborDict = dict ()

    is_loop=areConnected(app, app.StartGrid, app.endingPoint, mediumDict)
    while is_loop == False:
        #for a random ordered node in list of nodes
        for nodes in reqNodes:
            NeighborDict[nodes] = NeighborDict.get(nodes, [])
            if nodes not in app.tiles:
                app.tiles.append(nodes)
            (row, col) = nodes
            #pick random node neighbor
            n = mediumMode_pickRandomnodeNeighbor(app, row, col)
            if n  not in NeighborDict[nodes]:
                NeighborDict[nodes].append(n)
                if n not in app.tiles:
                    app.tiles.append(n)
                (r, c) = n
                #if they're not connected
                mediumDict = mediumMode_getDict(app)
                if areConnected (app, nodes, n, mediumDict) == False:
                    edge = (int((row + r)/2), int((col+c)/2))
                    (row1, col1) = edge
                #connect them
                    if 0 <= row1 < app.rows or 0 <= col1 < app.cols:
                        app.tiles.append(edge)
                #else: do nothing
        mediumDict = mediumMode_getDict(app)
        is_loop=areConnected(app, app.StartGrid, app.endingPoint, mediumDict) 
    return app.tiles.sort()

def hardMode_timerFired(app):
    if app.win == False:
        app.timeElapsed += app.timerDelay
        if app.gameOver == False:
            if app.timeElapsed % app.timeCheck == 0:
            #Keeping track of the rotation
                app.rotationCount += 1
                if app.rotationCount > 7:
                    app.rotationCount = 0

            #Changing color for tiles in color list
            elif app.timeElapsed - app.timeStarted > 2500:
                app.timeElapsed = 0
                if app.colorCount == True:
                    app.colorCount = False
                else:
                    app.colorCount = True

            #Keeping track of the special Tiles: side moving
            elif app.timeElapsed % 500 == 0:
                app.sideMovingCount += 1
                if app.sideMovingCount > 3:
                    app.sideMovingCount = 0
                #updating the tile in tile list with new tile everytime the
                #count is changed
                for index in app.sideMoving:
                    (x, y) = app.tiles[index]
                    (dx, dy) = app.sideMovingList[app.sideMovingCount]
                    app.tiles[index] = (x + dx, y+ dy)            

def hardMode_keyPressed(app, event): 
    if app.gameOver == False:
        if event.key == "Space":
            #checking if the cirle is on a tile
            rotationCountTemp = app.rotationCount
            if app.currentNeighbors[rotationCountTemp] in app.tiles:
                #app.sound.start()
                (x1, y1) = app.tiles[app.circlePosition + 1]
                value = app.tiles.index(app.currentNeighbors[rotationCountTemp])
                app.circlePosition = value - 1 
                (x, y) = app.tiles[app.circlePosition + 1]

                #Checking if the color of the circle is the same as color of the 
                #tile
                if (x, y) in app.colorChangingList:
                    if app.colorCount != app.color:
                        app.gameOver = True
                        app.win = False

                #Checking for fast tiles, increasing/ decreasing the speed
                if (x, y) in app.fast:
                    app.timeCheck = 75
                elif (x, y) in app.slow:
                    app.timeCheck = 300
                else: 
                    app.timeCheck = 150

                #checking for reverse tile, defining different trajectory
                if (x, y) in app.reverse:    
                    app.currentNeighbors = getReverseRotationalPath(app, x, y)
                else:
                    app.currentNeighbors = getRotationalPath(app, x, y)

                #if has reched ending point, player has won!
                if (x, y) == app.endingPoint:
                    app.gameOver = True
                    app.VictorySound.start()
                    app.win = True
                    app.currentNeighbors = []

                #color toggle, to switch between colors    
                if app.color == False:
                    app.color = True
                else:
                    app.color = False

                #Sidescrolling in all directions
                if (y - y1) > 0:
                    app.ScrollX += 25
                    app.ScrollY -= 25
                elif (y - y1) < 0:
                    app.ScrollX -= 25
                    app.ScrollY += 25
                elif (x - x1) > 0:
                    app.ScrollX += 25
                    app.ScrollY += 25
                elif (x - x1) < 0:
                    app.ScrollX -= 25
                    app.ScrollY -= 25

            #if not, wrong place
            else: 
               app.gameOver = True 
               #app.DeathSound.start() 
               app.win = False

    #To reset the game
    if event.key == "r" or event.key == "R":
        appStarted(app)          
            
def hardMode_redrawAll(app, canvas):
    #creating a background
    canvas.create_image(app.width, app.height, 
    image=ImageTk.PhotoImage(app.background2))
    if app.gameOver == False:
        #colour count for changing color tiles
        colorcount = app.colorCount
        for index in range(len(app.tiles)):
            #check if side moving
            (x, y) = app.tiles[index] 
            (x1, y1)= getStartingPoint(app, x, y)
            (x1, y1)= (x1-app.ScrollX, y1-app.ScrollY)

            if (x+1, y) not in app.tiles:
                drawHeightRight(app, canvas, x1, y1)
            if (x, y-1) not in app.tiles:
                drawHeightLeft(app, canvas, x1, y1)

        #drawing tiles for all points
        for index2 in range(len(app.tiles)):
            if app.tiles[index2] not in app.colorChangingList:
                (x, y) = app.tiles[index2]
                (x1, y1)= getStartingPoint(app, x, y)
                (x1, y1)= (x1-app.ScrollX, y1-app.ScrollY)
                drawTile(app,canvas, x1, y1) 

            #drawing color changing tiles   
            else:
                (x, y) = app.tiles[index2]
                (x1, y1)= getStartingPoint(app, x, y)
                (x1, y1)= (x1-app.ScrollX, y1-app.ScrollY)
                if colorcount == True:
                    color = app.colorChanging[0]
                else:
                    color = app.colorChanging[1]
                (x2, y2) = (x1 - app.Size, y1 - app.Size)
                (x3, y3) = (x1 , y1 - 2*app.Size) 
                (x4, y4) = (x1 + app.Size, y1 - app.Size)
                canvas.create_polygon(x1, y1, x2, y2,
                    x3, y3, x4, y4,
                    fill = color,
                    outline = 'white',
                    width = 1.2) 

        #drawing all special tiles
        #Fast tile
        for item in range(len(app.fast)):
            (x, y) = app.fast[item]
            (x1, y1)= getStartingPoint(app, x, y)
            (x1, y1)= (x1-app.ScrollX, y1-app.ScrollY)
            drawFlash(app, canvas, x1, y1)

        #Slow Tile
        for item2 in range(len(app.slow)):
            (x, y) = app.slow[item2]
            (x1, y1)= getStartingPoint(app, x, y)
            (x1, y1)= (x1-app.ScrollX, y1-app.ScrollY)
            drawSlow(app, canvas, x1, y1)

        #Reverse tile
        for item3 in range(len(app.reverse)):
            (x, y) = app.reverse[item3]
            (x1, y1)= getStartingPoint(app, x, y)
            (x1, y1)= (x1-app.ScrollX, y1-app.ScrollY)
            drawReverse(app, canvas, x1, y1)

        #drawing circles2 and 1
        if app.circlePosition < len(app.tiles)-1:
                (row, col) = app.currentNeighbors[app.rotationCount]
                (x, y) = getStartingPoint(app, row, col)
                (x, y)= (x-app.ScrollX, y-app.ScrollY)
                (x2, y2) = app.tiles[app.circlePosition + 1]
                (x3, y3)= getStartingPoint(app, x2, y2)
                (x3, y3)= (x3-app.ScrollX, y3-app.ScrollY)

                if app.color == True:
                    drawCircle1(app, canvas, x, y)
                    drawCircle2(app, canvas, x3, y3)

                else:
                    drawCircle2(app, canvas, x, y)
                    drawCircle1(app, canvas, x3, y3)

    #if circle has not landed on a tile or if the player wins
    else:
        if app.win == True:
            canvas.create_rectangle(0,0,app.width, app.height, fill= "black")
            canvas.create_text(app.width/2, app.height/2, fill= "white",
                           text= "You have won!", font= f'Arial 30 bold')
        else:
            canvas.create_rectangle(0,0,app.width, app.height, fill= "black")
            canvas.create_text(app.width/2, app.height/2, fill= "White",
                           text= "Game Over, Press R to restart", 
                           font=f'Arial 30 bold')

def runGame():
    runApp(width=800, height=800)


def main():
    runGame()


if (__name__ == '__main__'):
    main()


