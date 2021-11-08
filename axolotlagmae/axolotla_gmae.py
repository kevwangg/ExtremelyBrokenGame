import tkinter
from types import prepare_class
from cmu_112_graphics import *
import pygame

class Sound(object):
    def __init__(self, path):
        self.path = path
        self.loops = 1
        pygame.mixer.music.load(path)



    # Loops = number of times to loop the sound.
    # If loops = 1 or 1, play it once.
    # If loops > 1, play it loops + 1 times.
    # If loops = -1, loop forever.
    def start(self, loops=1):
        self.loops = loops
        pygame.mixer.music.play(loops=loops)

    def stop(self):
        pygame.mixer.music.stop()








def appStarted(app):
    app.cx = 75
    app.cy = 420
    app.r = 30
    app.timerDelay = 20
    app.onGround = True
    app.image1 = app.loadImage('koz.png')
    app.koz = app.scaleImage(app.image1, 0.1)
    app.image2 = app.loadImage('tay.png')
    app.tay = app.scaleImage(app.image2, 0.6)
    app.realtay = app.tay.transpose(Image.FLIP_LEFT_RIGHT)
    app.level = 0
    app.section = 0
    app.mapList = [(CUC1, CUC2, CUC3), (ham1, ham2, ham3)]
    app.circleList = []
    app.image3 = app.loadImage('cohon.png')
    app.image4 = app.loadImage('ham.png')
    app.cohon = app.scaleImage(app.image3, 1.5)
    app.ham = app.scaleImage(app.image4, 1)
    app.backgroundList = [app.cohon, app.ham]
    app.image5 = app.loadImage('bigC.png')
    app.bigC = app.scaleImage(app.image5, 2)
    app.bigCReal = app.bigC.transpose(Image.FLIP_LEFT_RIGHT)
    app.bossList = [app.bigCReal]
    app.bossCounter = 5
    app.image7 = app.loadImage('axosakdo.png')
    app.axoloto = app.scaleImage(app.image7, 1)
    pygame.mixer.init()
    app.sound = Sound("kosbie.mp3")
    app.winImage = app.loadImage('win.png')
    app.win = app.scaleImage(app.winImage, 1)


def drawMap(app, canvas):
    canvas.create_image(500, 250, image=ImageTk.PhotoImage(app.backgroundList[app.level]))
    canvas.create_rectangle(0, 450, 1000, 500, fill='green')


def keyPressed(app, event):
    if (event.key == "Right"):
            app.cx += 5
            isLegalPlayerMove(app)
            if app.cx >= 0.9 * app.width:
                app.circleList = []
                if (app.section + 1) == 3:
                    app.section = 1
                    app.level += 1
                else:
                    app.section += 1
                    app.cx = 75
    if (event.key == "Left"):
            app.cx -= 5
            isLegalPlayerMove(app)
    if (event.key == "Up"):
            if app.onGround == False:
                return
            app.cy -= 100
            app.onGround = False
            isLegalPlayerMove(app)
    if (event.key == "Space"):
            app.cx += 60
            isLegalPlayerMove(app)
            if app.cx >= 0.9 * app.width:
                app.circleList = []
                if (app.section + 1) == 3:
                    app.section = 0
                    app.level += 1
                    app.bossList.append(app.bigCReal)
                    app.bossCounter = 10
                    app.cx = 75
                else:
                    app.section += 1
                    app.cx = 75
    if (event.key == 'x'):
        app.circleList.append([app.cx, app.cy-app.r-15])
    if (event.key == 'z'):
        app.circleList.append([app.cx+app.r+10, app.cy])
    if (event.key == 'm'):
        app.sound.start(loops=-1)
    if (event.key == 'r'):
        runGame()


def isLegalMove(app):
    if app.cy + 2 <= 420:
        return True
    else:
        return False

def isLegalPlayerMove(app):
    if app.level == 0 and app.section == 0:
        if ((400-app.r < app.cx <= 500+app.r) and (app.cy > 380-app.r)):
            app.cx, app.cy = 400-app.r, 380-app.cy
        if ((500-app.r < app.cx < 600+app.r) and (app.cy > 300-app.r)):
            app.cx, app.cy = 500-app.r, 380-app.cy
        if ((700-app.r <= app.cx <= 800+app.r) and (app.cy  >= 300-app.r)):
            app.cx, app.cy = 700-app.r, 380-app.cy
        if ((800-app.r <= app.cx <= 900+app.r) and (app.cy >= 380-app.r)):
            app.cx, app.cy = 800-app.r, 380-app.cy


def timerFired(app):
    if isLegalMove(app):
        app.cy += 5
    if (app.cy+app.r == 450):
        app.onGround = True
    for circle in app.circleList:
        circle[0] += 10
        if circle[0] >= 1000:
            app.bossCounter -= 1
            app.circleList.remove(circle)
            if app.bossCounter == 0:
                app.bossList.pop()
 


def drawChar(app, canvas):
    canvas.create_image(app.cx, app.cy, image=ImageTk.PhotoImage(app.axoloto))
    #canvas.create_oval(app.cx-app.r, app.cy-app.r, app.cx+app.r, app.cy+app.r, fill='red')
    canvas.create_image(app.cx+app.r+10, app.cy, image=ImageTk.PhotoImage(app.realtay))
    canvas.create_image(app.cx, app.cy-app.r-15, image=ImageTk.PhotoImage(app.koz))

def drawBoss(app, canvas):
    if app.bossList != []:
        canvas.create_image(900, 450, image=ImageTk.PhotoImage(app.bossList[0]))


def redrawAll(app, canvas):
    if app.level == 2:
        app.sound.stop()
        canvas.create_image(500, 250, image=ImageTk.PhotoImage(app.win))
    else:
        drawMap(app, canvas)
        drawChar(app, canvas)
        app.mapList[app.level][app.section](app, canvas)
        if app.section == 2:
            drawBoss(app, canvas)
        drawProjectiles(app, canvas)
        canvas.create_text(500, 50, text='We got 8+ Hours of Sleep', fill='Blue', font='Times 50 bold')
        canvas.create_text(500,  460, text='Bottom Text', fill='Blue', font='Times 50 bold')
    

def drawProjectiles(app, canvas):
    r = 10
    for circle in app.circleList:
        canvas.create_oval(circle[0]-r, circle[1]-r, circle[0]+r, circle[1]+r, fill='yellow')

def CUC1(app, canvas):
    canvas.create_rectangle(400, 380, 500, 450, fill = "yellow")
    canvas.create_rectangle(500, 300, 600, 450, fill = "yellow")
    
    canvas.create_rectangle(700, 300, 800, 450, fill = "yellow")
    canvas.create_rectangle(800, 380, 900, 450, fill = "yellow")

def CUC2(app, canvas):
    canvas.create_rectangle(200, 300, 300, 370, fill = "yellow")
    canvas.create_rectangle(400, 230, 500, 300, fill = "yellow")
    
    canvas.create_rectangle(600, 300, 700, 370, fill = "yellow")
    canvas.create_rectangle(800, 380, 900, 450, fill = "yellow")


def CUC3(app, canvas):
    pass

def ham1(app, canvas):
    canvas.create_rectangle(200, 200, 350, 225, fill = "yellow")
    canvas.create_rectangle(200, 350, 350, 375, fill = "yellow")
    
    canvas.create_rectangle(500, 380, 550, 450, fill = "yellow")
    canvas.create_rectangle(550, 340, 600, 450, fill = "yellow")
    canvas.create_rectangle(600, 300, 650, 450, fill = "yellow")

    canvas.create_rectangle(750, 300, 800, 450, fill = "yellow")
    canvas.create_rectangle(800, 340, 850, 450, fill = "yellow")
    canvas.create_rectangle(850, 380, 900, 450, fill = "yellow")
    
def ham2(app, canvas):
    canvas.create_rectangle(200, 300, 300, 370, fill = "yellow")
    canvas.create_rectangle(400, 380, 500, 450, fill = "yellow")
    
    canvas.create_rectangle(600, 300, 700, 370, fill = "yellow")
    canvas.create_rectangle(800, 230, 900, 300, fill = "yellow")

def ham3(app, canvas):
    canvas.create_rectangle(200, 380, 300, 450, fill = "yellow")
    canvas.create_rectangle(400, 300, 500, 370, fill = "yellow")

def runGame():
    runApp(width=1000, height=500)

runGame()