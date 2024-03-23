from Classes import *
from cmu_graphics import *
import copy 
from GameImages import images


def createUIMonkeys():
    x = 847
    y = 92
    dx = 0
    dy = 0
    i = 0
    for monkeys in tStats:
        match i:
            case 0:
                dx = 0
            case 1:
                dx = 100
        monkey = UITower(x + dx, y + dy, monkeys)
        i += 1
        if i % 2 == 0:
            i = 0
            dy += 200



def onAppStart(app):
    ### DO NOT CHANGE, EVERYTHING WILL BREAK ###
    app.width = 1000
    app.height = 800

    app.waveNum = 1
    app.stepsPerSecond = 50

    app.difficulty = 1
    app.playerHealth = 125 
    app.playerMoney = 450
    app.slowOrFast = True 
    app.startCash = None
    app.startLives = None

    app.selected = None 
    createUIMonkeys()

    app.playing = False

def turnerSetEasy():
    turner = Turn(404, 255, 15, 'up')
    turner = Turn(399, 103, 15, 'left')
    turner = Turn(250, 112, 15, 'down')
    turner = Turn(260, 496, 15, 'left')
    turner = Turn(120, 489, 15, 'up')
    turner = Turn(132, 341, 15, 'right')
    turner = Turn(514, 346, 15, 'up')
    turner = Turn(514, 186, 15, 'right')
    turner = Turn(612, 195, 15, 'down')
    turner = Turn(608, 446, 15, 'left')
    turner = Turn(342, 439, 15, 'down')

def turnerSetMedium():
    pass

def turnerSetHard():
    pass






################################ Start Screen ##################################

def start_redrawAll(app):
        drawScreen0(app)

def drawScreen0(app):
    drawImage(images[0], app.width/2, app.height/2, align = 'center', 
              width = app.width, height = app.height)
    drawRect(app.width / 2, 3*app.height/4, 200, 50, align = 'center', fill = 'white', opacity = 75, 
             border = 'black')
    drawLabel('Press Anywhere To Play!', app.width / 2, 3*app.height/4, size = 16, bold = True)

def start_onMousePress(app, mouseX, mouseY):
    setActiveScreen('mapSelect')

############################## Map Selector Screen #############################

def mapSelect_redrawAll(app):
        drawScreen1(app)

def drawScreen1(app):
    mapWidth, mapHeight = getImageSize(images[1])
    drawImage(gameIcons[1][app.difficulty], app.width/2, app.height/2, align = 'center',
              width=mapWidth//2.5, height=mapHeight//2.5 - 9)
    drawRect(app.width/2, app.height/2, 320, 232, align = 'center', fill = None, 
             border = 'black', borderWidth = 5)
    imageWidth2, imageHeight2 = getImageSize(images[4])

    #Right Arrow 
    imageWidth, imageHeight = getImageSize(images[2])
    drawImage(images[2], 3*app.width/4, app.height/2, align = 'center', 
              width = imageWidth // 3, height = imageHeight // 3)
    
    #Left Arrow
    drawImage(images[3], app.width/4, app.height/2, align = 'center', 
              width = imageWidth // 3, height = imageHeight // 3)
    
    #Play Button 
    imageWidth2, imageHeight2 = getImageSize(images[4])
    drawImage(images[4], app.width // 2, 3.5*app.height//4, align = 'center', 
              width = imageWidth2 // 2, height = imageHeight2 // 2)

def mapSelect_onMousePress(app, mouseX, mouseY):
    if clickedLeft(mouseX, mouseY):
        if app.difficulty > 0:
            app.difficulty -= 1
    elif clickedRight(mouseX, mouseY):
        if app.difficulty < 2:
            app.difficulty += 1
    elif clickedPlay(mouseX, mouseY):
        diff = app.difficulty
        match diff:
            case 0:
                app.startCash = 100000
                app.startLives = 150
                turnerSetEasy()
            case 1:
                app.startCash = 650
                app.startLives = 125
                turnerSetMedium()
            case 2:
                turnerSetHard()
                app.startCash = 500
                app.startLives = 100
        setActiveScreen('game')

def clickedLeft(mX, mY):
    if 222 <= mX <= 278 and 372 <= mY <= 428:
        return True 

def clickedRight(mX, mY):
    if 722 <= mX <= 778 and 372 <= mY <= 428:
        return True 

def clickedPlay(mX, mY):
    if 436 <= mX <= 564 and 620 <= mY <= 780:
        return True 

################################ Game Screen ###################################

def game_redrawAll(app):
        drawMap(app)
        drawBloons(app)
        drawTowers(app)
        drawUpgradeBox(app)
        drawProjectiles(app)

def drawMap(app):
    image = gameIcons[1][app.difficulty]
    drawImage(image, 0, 0)
    drawImage(images[6], 800, 0)
    drawLabel(f'Health: {app.startLives}', 40, 10, bold = True, size = 16, fill = 'pink')
    drawLabel(f'Cash: {app.startCash}', 35, 30, bold = True, size = 16, fill = 'pink')
    drawUIMonkeys(app)

def drawUIMonkeys(app):
    for monkey in UITower.registry:
        drawImage(tStats[monkey.name][4], monkey.x, monkey.y, align = 'center')
        drawRect(monkey.x, monkey.y, 50, 50, border = 'black', fill = None, 
                 align = 'center', borderWidth = 3)
        drawLabel(monkey.name, monkey.x, monkey.y + 40, bold = True)
        drawLabel(monkey.cost, monkey.x, monkey.y + 60, bold = True)

def drawBloons(app):
    for bloons in Balloon.registry:
        drawImage(bloons.color, bloons.x, bloons.y, align = 'center')
        # drawCircle(bloons.x, bloons.y, 10, fill = bloons.color)
        for turner in Turn.registry:
            if distance(bloons.x, bloons.y, turner.x, turner.y) <= 10:
                bloons.d = turner.d

def drawTowers(app):
    for tower in Tower.registry:
        drawImage(tStats[tower.name][4], tower.x, tower.y, align = 'center', rotateAngle = tower.rotation)
        drawCircle(tower.x, tower.y, tower.range, fill = None, border = 'black')
        if not tower.isMoving:
            tower.getBloonsInRange()
            tower.doDamage()

def drawUpgradeBox(app):
    drawImage(images[5], 0, 600)
    if isinstance(app.selected, Tower): 
        match app.selected.name:
            case 'dart':
                drawImage(gameIcons[0], 50, 625)
            case 'bomb':  #3
                drawImage(gameIcons[3], 50, 625)
            case 'spinny': #5
                drawImage(gameIcons[5], 50, 625)
            case 'glue': #2
                drawImage(gameIcons[2], 50, 625)
            case 'ninja': #4 
                drawImage(gameIcons[4], 50, 625)
        

def drawProjectiles(app):
    for proj in Projectile.registry:
        drawImage(projStats[proj.parentTower][2], proj.x, proj.y, rotateAngle = proj.rotation)

def game_onStep(app):
    createWave(app, app.waveNum)
    for proj in Projectile.registry:
        proj.move(app)
    for bloon in Balloon.registry:
        bloon.move(app)

def createWave(app, wave):
    if checkIfClear(app) and app.playing:
        if wave > 1:
            match app.difficulty:
                case 0:
                    app.startCash += 120
                case 1:
                    app.startCash += 160
                case 2:
                    app.startCash += 200
        i = 0
        if wave < len(bloonList):
            for bloon in bloonList[wave]:
                bloons = Balloon((i * -15) - 10, 255, bloon, 'right')
                print(Balloon.registry)
                i += 1
        else:
            spawnList = []
            currRound = randomRound(app.waveNum, spawnList)
            print(currRound)
            for bloon in currRound:
                print(bloon)
                bloons = Balloon((i * -15) - 10, 255, bloon, 'right')
                print(Balloon.registry)
                i += 1
        app.waveNum += 1

def checkIfClear(app):
    if Balloon.registry == []:
        return True 
    return False

def game_onMousePress(app, mouseX, mouseY):
    print(Projectile.registry)
    clickedOnUITower(app, mouseX, mouseY)
    if app.selected == None:
        clickedOnTower(app, mouseX, mouseY)

def clickedOnUITower(app, mx, my):
    for monkey in UITower.registry:
        if distance(mx, my, monkey.x, monkey.y) <= 30 and app.startCash >= monkey.cost:
            app.selected = Tower(monkey.x, monkey.y, monkey.name)
            app.startCash -= monkey.cost 
            return
        app.selected = None

def clickedOnTower(app, mx, my):
    for tower in Tower.registry:
        if distance(mx, my, tower.x, tower.y) <= 30:
            app.selected = tower
            return 
    app.selected = None

def game_onMouseMove(app, mouseX, mouseY):
    print(mouseX, mouseY)

def game_onMouseDrag(app, mouseX, mouseY):
    moveTower(app, mouseX, mouseY)
    app.stepsPerSecond = 50

def moveTower(app, mx, my):
    if isinstance(app.selected, Tower) and not app.selected.placed:
        app.selected.x = mx
        app.selected.y = my
        app.selected.isMoving = True 

def game_onMouseRelease(app, mouseX, mouseY):
    if isinstance(app.selected, Tower):
        if app.selected.x >= 800 or app.selected.y >= 600:
            app.startCash += app.selected.cost
            Tower.registry.remove(app.selected) 
        app.selected.placed = True
        app.selected.isMoving = False

def game_onKeyPress(app, key):
    if key == 'p':
        if app.slowOrFast:
            app.stepsPerSecond = 25
        else:
            app.stepsPerSecond = 50
        app.slowOrFast = not app.slowOrFast 
    if key == 's':
        if not app.playing:
            app.playing = True
    if isinstance(app.selected, Tower):
        if key == 'backspace':
            app.startCash += (2*app.selected.cost)//3
            Tower.registry.remove(app.selected)
        elif key == '<' or key == ',':
            app.selected.upgrade('left', app)
        elif key == '>' or key == '.':
            app.selected.upgrade('right', app)
        print(app.selected.leftPath, app.selected.rightPath)
    
#------------------------------------------------------------------------------#

runAppWithScreens(initialScreen='start')