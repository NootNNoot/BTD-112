from Classes import *
from cmu_graphics import *
from GameImages import images
from Upgrades import *
import random 


def onAppStart(app):
    ### DO NOT CHANGE, EVERYTHING WILL BREAK ###
    app.width = 1000
    app.height = 800
    app.stepsPerSecond = 50
    app.difficulty = 0
    createUIMonkeys()
    fullReset(app)

def fullReset(app):
    app.waveNum = 1
    app.playerHealth = None
    app.playerMoney = None
    app.slowOrFast = True 
    app.startCash = None
    app.startLives = None
    app.selected = None 
    app.lost = False
    app.playing = False
    app.paused = False

#Turning Points for Easy Map 
def turnerSetEasy():
    turnerE = Turn(410, 252, 15, 'up')
    turnerE = Turn(410, 112, 15, 'left')
    turnerE = Turn(250, 112, 15, 'down')
    turnerE = Turn(260, 496, 15, 'left')
    turnerE = Turn(120, 489, 15, 'up')
    turnerE = Turn(132, 341, 15, 'right')
    turnerE = Turn(514, 346, 15, 'up')
    turnerE = Turn(514, 186, 15, 'right')
    turnerE = Turn(612, 195, 15, 'down')
    turnerE = Turn(608, 446, 15, 'left')
    turnerE = Turn(342, 439, 15, 'down')

#Turning Points for Hard Map 
def turnerSetHard():
    turnerH = Turn(129, 273, 15, 'up')
    turnerH = Turn(129, 174, 15, 'up-right')
    turnerH = Turn(170, 140, 15, 'right')
    turnerH = Turn(238, 140, 15, 'down-right')
    turnerH = Turn(304, 221, 15, 'down')
    turnerH = Turn(304, 284, 15, 'right')
    turnerH = Turn(479, 284, 15, 'down')
    turnerH = Turn(479, 353, 15, 'down-right')
    turnerH = Turn(537, 410, 15, 'right')
    turnerH = Turn(594, 410, 15, 'up-right')
    turnerH = Turn(647, 338, 15, 'up')
    turnerH = Turn(647, 271, 15, 'right')

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
    #Background
    drawImage(images[7], app.width/2, app.height/2, align = 'center')

    #Draws either of the maps in a preview style depending on what difficulty 
    #is selected 
    mapWidth, mapHeight = getImageSize(images[1])
    drawImage(gameIcons[1][app.difficulty], app.width/2, app.height/2, align = 'center',
              width=mapWidth//2.5, height=mapHeight//2.5 - 9)
    drawRect(app.width/2, app.height/2, 320, 232, align = 'center', fill = None, 
             border = 'black', borderWidth = 5)
    
    #Labels for maps:
    difficulty = 'Easy' if app.difficulty == 0 else 'Hard'
    lives = 150 if app.difficulty == 0 else 100
    cash = 650 if app.difficulty == 0 else 500
    drawLabel(f'Difficulty: {difficulty}', app.width/2, app.height/4, bold=True, 
              size=20, fill='white', border='black', borderWidth=1)
    drawLabel(f'Starting Lives: {lives}', app.width/2, app.height/4 + 20, bold=True, 
              size=20, fill='white', border='black', borderWidth=1)
    drawLabel(f'Starting Cash: {cash}', app.width/2, app.height/4 + 40, bold=True, 
              size=20, fill='white', border='black', borderWidth=1)

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
        if app.difficulty < 1:
            app.difficulty += 1
    elif clickedPlay(mouseX, mouseY):
        match app.difficulty:
            case 0:
                app.startCash = 650
                app.startLives = 150
                turnerSetEasy()
            case 1:
                app.startCash = 1000
                app.startLives = 100
                turnerSetHard()
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
        if app.lost:
            drawLossScreen(app)
        if app.paused:
            drawPause(app)

def drawLossScreen(app):
    drawRect(app.width/2, app.height/2, 1000, 800, fill = 'darkgray', opacity = 85, align = 'center')
    drawLabel('YOU LOST', app.width/2, app.height/2, size = 32, fill='red', border='black', bold = True)
    drawImage(images[8], app.width/2 + 50, app.height/2 + 50, align = 'center')
    drawImage(images[9], app.width/2 - 50, app.height/2 + 50, align = 'center')
    
def drawPause(app):
    drawRect(app.width/2, app.height/2, 1000, 800, fill = 'darkgray', opacity = 85, align = 'center')
    drawLabel('PAUSED', app.width/2, app.height/2, size = 32, fill='blue', border='black', bold = True)
    drawImage(images[8], app.width/2 + 50, app.height/2 + 50, align = 'center')
    drawImage(images[9], app.width/2 - 50, app.height/2 + 50, align = 'center')

def drawMap(app):
    image = gameIcons[1][app.difficulty]
    drawImage(image, 0, 0)
    drawImage(images[6], 800, 0)
    drawLabel(f'Health: {app.startLives}', 856, 35, bold = True, size = 18, align = 'center')
    drawLabel(f'Cash: {app.startCash}', 956, 35, bold = True, size = 18, align = 'center')
    drawLabel(f'Round: {app.waveNum - 1}', 900, 700, bold = True, size = 24, align = 'center')
    drawUIMonkeys(app)
    drawLabel("Press 'space' To Start The Game", 900, 605, bold = True, size = 13)
    drawLabel("Press 'escape' To Pause", 900, 620, bold = True, size = 13)
    drawLabel("Press 'p' To Change Speed", 900, 635, bold = True, size = 13)
    drawLabel("Press 'backspace' to Sell", 900, 650, bold = True, size = 13)
    drawLabel("A Tower For 2/3 Value", 900, 665, bold = True, size = 13)

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
        for turner in Turn.registry:
            if distance(bloons.x, bloons.y, turner.x, turner.y) <= 15:
                bloons.d = turner.d

def drawTowers(app):
    for tower in Tower.registry:
        drawImage(tStats[tower.name][4], tower.x, tower.y, align = 'center', rotateAngle = tower.rotation)
        if not tower.isMoving:
            tower.getBloonsInRange()
            tower.doDamage()

def drawUpgradeBox(app):
    drawImage(images[5], 0, 600)
    
    if isinstance(app.selected, Tower): 
        drawCircle(app.selected.x, app.selected.y, app.selected.range, fill = None, border = 'black')
        drawLabel(app.selected.name, 120, 615, bold=True, size=20)
        drawLabel('Sell Value:', 269, 615, bold=True, size=20)
        drawLabel((2*app.selected.cost)//3, 269, 635, bold=True, size=20)
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
        drawLeftUpgrade(app)
        drawRightUpgrade(app)
    
def drawLeftUpgrade(app):
    type, amount, cost = leftUpgrades[app.selected.name][app.selected.leftPath]
    if app.selected.rightFinalUpgrade == True and app.selected.leftPath == 2:
        drawImage(upgradeImages['restricted'], 330, 625)
    else:    
        drawImage(upgradeImages[type], 330, 625)
        if type != None:
            drawLabel(f'Cost = {cost}', 405, 615, bold = True, size = 20)
            drawLabel(f'Upgrades {type} by {amount}', 405, 770, size = 16, bold = True)
    

def drawRightUpgrade(app):
    type, amount, cost = rightUpgrades[app.selected.name][app.selected.rightPath]
    if app.selected.leftFinalUpgrade == True and app.selected.rightPath == 2:
        drawImage(upgradeImages['restricted'], 530, 625)
    else:
        drawImage(upgradeImages[type], 530, 625)
        if type != None:
            drawLabel(f'Cost = {cost}', 605, 615, bold = True, size = 20)
            drawLabel(f'Upgrades {type} by {amount}', 605, 770, size = 16, bold = True)
    
def drawProjectiles(app):
    for proj in Projectile.registry:
        drawImage(projStats[proj.parentTower][2], proj.x, proj.y, rotateAngle = proj.rotation)

def game_onStep(app):
    if app.lost == True or app.paused == True:
        return 
    if app.startLives <= 0:
        app.lost = True 
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
        if wave < len(bloonList):
            makeWave(app, bloonList[wave])
        else:
            spawnList = []
            currRound = randomRound(app.waveNum, spawnList)
            makeWave(app, currRound)
        app.waveNum += 1

def makeWave(app, list):
    i = 0
    match app.difficulty:
        case 0:
            for bloon in list:
                bloons = Balloon((i * -15) - 10, 255, bloon, 'right')
                i += 1
        case 1:
            for bloon in list:
                bloons = Balloon((i * -15) - 10, 277, bloon, 'right')
                i += 1

def checkIfClear(app):
    if Balloon.registry == []:
        return True 
    return False

def randomRound(wave, spawnList, amountEach = 0):
    if wave < 40:
        amountEach = 10
    if wave < 50:
        amountEach = 15
    for i in range(1, len(eStats) + 1):
            totalSpawn = random.randrange(1, amountEach + 1)
            spawnList += [i for j in range(totalSpawn)]
    return spawnList

def game_onMousePress(app, mouseX, mouseY):
    if not app.lost:
        clickedOnUITower(app, mouseX, mouseY)
        clickedOnTower(app, mouseX, mouseY)
        if isinstance(app.selected, Tower):
            clickedOnUpgradeLeft(app, mouseX, mouseY)
            clickedOnUpgradeRight(app, mouseX, mouseY)
    if app.lost or app.paused:
        if 422 <= mouseX <= 478 and 422 <= mouseY <= 478:
            goHome(app)
        elif 502 <= mouseX <= 556 and 422 <= mouseY <= 478:
            restart(app)

def goHome(app):
    fullReset(app)
    app.difficulty = 0
    resetClasses()
    setActiveScreen('mapSelect')

def restart(app):
    fullReset(app)
    resetClasses()
    match app.difficulty:
        case 0:
            app.startCash = 650
            app.startLives = 150
            turnerSetEasy()
        case 1:
            app.startCash = 500
            app.startLives = 100
            turnerSetHard()

def resetClasses():
    Balloon.registry = []
    Tower.registry = []
    Turn.registry = []

def clickedOnUITower(app, mx, my):
    for monkey in UITower.registry:
        if distance(mx, my, monkey.x, monkey.y) <= 30 and app.startCash >= monkey.cost:
            app.selected = Tower(monkey.x, monkey.y, monkey.name)
            app.startCash -= monkey.cost 

def clickedOnTower(app, mx, my):
    for tower in Tower.registry:
        if distance(mx, my, tower.x, tower.y) <= 30:
            app.selected = tower
            return 
    if (0 <= mx <= 800) and (0 <= my <= 600):
        app.selected = None 

def clickedOnUpgradeLeft(app, mx, my):
    if 330 <= mx <= 480 and 625 <= my <= 785:
        app.selected.upgrade('left', app)


def clickedOnUpgradeRight(app, mx, my):
    if 530 <= mx <= 680 and 625 <= my <= 785:
        app.selected.upgrade('right', app)

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
            app.selected = None
            return
        app.selected.placed = True
        app.selected.isMoving = False

def game_onKeyPress(app, key):
    if key == 'p':
        if app.slowOrFast:
            app.stepsPerSecond = 25
        else:
            app.stepsPerSecond = 50
        app.slowOrFast = not app.slowOrFast 
    if key == 'space':
        if not app.playing:
            app.playing = True
    if key == 'escape':
        app.paused = not app.paused
        print(app.paused)
    if isinstance(app.selected, Tower):
        if key == 'backspace':
            app.startCash += (2*app.selected.cost)//3
            Tower.registry.remove(app.selected)
            app.selected = None
        elif key == '<' or key == ',':
            app.selected.upgrade('left', app)
        elif key == '>' or key == '.':
            app.selected.upgrade('right', app)
    
#------------------------------------------------------------------------------#

runAppWithScreens(initialScreen='start')