from enemyStats import *
from towerStats import *
from cmu_graphics import *
from ProjectileStats import *
from Upgrades import *
from utils import *

#Contains classes used in the program 


#------------------------------------------------------------------------------#

class Balloon:
    registry = []
    id = 0

    def __init__(self, x, y, num, direction):
        self.health = eStats[num][0] 
        self.speed = eStats[num][1]
        self.color  = eStats[num][2]
        self.resistances = eStats[num][4]
        self.bloonNumber = num
        self.type = type 
        self.id = Balloon.id
        self.d = direction
        Balloon.id += 1
        Balloon.registry.append(self)
        self.x = x
        self.y = y
        self.traits = []
        self.justHit = True

    def __repr__(self):
        return f'{self.id}'

    def __hash__(self):
        return hash(self.id)

    #Changes a bloons stats when it gets damaged (mimiks popping)
    def changeBloon(self):
        if self.health > 0:
            self.health = eStats[self.health][0]
            self.color  = eStats[self.health][2]
    
    def checkForChildren(self, amount, spawnList):
        if 'special' in eStats[self.bloonNumber]:
            if self.health < eStats[self.bloonNumber - 1][0]:
                bloonsToAdd = []
                i = 1
                for child in eStats[self.bloonNumber][3]:
                    spawnList.append((child, self.x, self.y, self.d))
                Balloon.registry.remove(self)

    def damageBasedOnType(self, amount, type, app):
        bloonsToSpawn = []
        if type == 'physical' and type not in self.resistances:
            self.health -= amount 
            app.startCash += amount 
            self.changeBloon()
            self.checkForChildren(amount, bloonsToSpawn)
        elif type == 'explosion' and type not in self.resistances:
            hit = 0
            for bloons in Balloon.registry:
                if distance(self.x, self.y, bloons.x, bloons.y) <= 20 and hit < 5:
                    bloons.health -= amount
                    app.startCash += amount 
                    hit += 1
                    bloons.changeBloon()
                    bloons.checkForChildren(amount, bloonsToSpawn)
        elif type == 'glue' and not self.hasStatus() and type not in self.resistances:
            self.traits.append('glue')
            self.health -= amount 
            app.startCash += amount 
            self.changeBloon()
            self.checkForChildren(amount, bloonsToSpawn)
        spawnNewBloons(bloonsToSpawn)
    
    def damage(self, amount, type, app):
        self.damageBasedOnType(amount, type, app)
    
    #Checks if a bloon has a status to slow it down or if it is dead 
    def checkStatus(self):
        if self.health <= 0:
            Balloon.registry.remove(self)
            return
        if 'glue' in self.traits:
            self.speed = eStats[self.bloonNumber][1] / 2
        else:
            self.speed = eStats[self.bloonNumber][1]

    def hasStatus(self):
        if self.traits == []:
            return False
        return True

    def move(self, app):
        self.checkStatus()
        if (self.x > 790 or 0 > self.y or self.y > 600):
            app.startLives -= self.health
            Balloon.registry.remove(self)
            return 
        direction = self.d
        match direction: 
            case 'right':
                self.x += self.speed
            case 'left':
                self.x -= self.speed
            case 'up':
                self.y -= self.speed
            case 'down':
                self.y += self.speed
            case 'up-right':
                self.x += self.speed
                self.y -= self.speed
            case 'up-left':
                self.x -= self.speed
                self.y -= self.speed
            case 'down-left':
                self.y += self.speed
                self.x -= self.speed
            case 'down-right':
                self.y += self.speed
                self.x += self.speed
        
#------------------------------------------------------------------------------#

class Tower:
    registry = []
    id = 0

    def __init__(self, x, y, monkey):
        self.damage = tStats[monkey][0]
        self.range = tStats[monkey][1]
        self.aps = tStats[monkey][2]
        self.type = tStats[monkey][3]
        self.icon = tStats[monkey][4]
        self.pierce = tStats[monkey][5]
        self.cost = tStats[monkey][6]
        self.upgrades = []
        self.leftPath = self.rightPath = 0
        self.name = monkey 
        self.id = Tower.id
        self.x = x
        self.y = y
        Tower.registry.append(self)
        Tower.id += 1
        self.sinceLast = 0 #Time since last attack
        self.bloonsInRange = []
        self.isMoving = False
        self.placed = False
        self.priority = 'first'
        self.rotation = 180
        self.attacksPerAttack = tStats[monkey][7]
        self.leftFinalUpgrade = False
        self.rightFinalUpgrade = False


    def __repr__(self):
        return f'{self.id}'
    
    def __eq__(self, other):
        if isinstance(other, Tower) and other.id == self.id:
            return True
        return False

    def __hash__(self):
        return hash(self.id)

    #CITATION - I got this formula and code from 
    #https://stackoverflow.com/questions/2676719/calculating-the-angle-between-a-line-and-the-x-axis
    #by user kingrichard2005 
    def changeAngle(self, bloon):
        angle = (math.atan2(bloon.y - self.y, bloon.x - self.x) * 180/math.pi) + 90
        self.rotation = angle

    def doDamage(self):
        for bloon in self.bloonsInRange:
            if self.sinceLast >= self.aps and exists(bloon):
                self.changeAngle(bloon)
                for i in range(self.attacksPerAttack):
                    self.shootProjectile(bloon, i)
                self.bloonsInRange.remove(bloon)
                self.sinceLast = 0
            elif self.type == 'glue':
                if bloon.hasStatus():
                    self.bloonsInRange.remove(bloon)
            elif not exists(bloon):
                self.bloonsInRange.remove(bloon)
    
    def shootProjectile(self, bloon, i):
        currProj = Projectile(self.x + 10*i, self.y, bloon.x + 10*i, bloon.y, self, bloon)

    def getBloonsInRange(self):
        self.sinceLast += .012
        for bloon in Balloon.registry:
            if bloon in self.bloonsInRange or not exists(bloon):
                if distance(self.x, self.y, bloon.x, bloon.y) > self.range:
                    self.bloonsInRange.remove(bloon)
            elif (distance(self.x, self.y, bloon.x, bloon.y) <= self.range):
                self.bloonsInRange.append(bloon)

    def upgrade(self, side, app):
        #Makes sure one side is capped at 2 upgrades
        if self.leftPath == 4:
            self.leftFinalUpgrade = True
        if self.rightPath == 4:
            self.rightFinalUpgrade = True
        if (side == 'left' and ((self.rightPath <= 2 or self.leftPath <= 1) and 
              not self.leftFinalUpgrade)):
            type, amount, cost = leftUpgrades[self.name][self.leftPath]
            self.doUpgradeLeft(app, type, amount, cost)
        elif (side == 'right' and ((self.leftPath <= 2 or self.rightPath <= 1) and 
              not self.rightFinalUpgrade)): 
            type, amount, cost = rightUpgrades[self.name][self.rightPath]
            self.doUpgradeRight(app, type, amount, cost)


    def doUpgradeRight(self, app, type, amount, cost):
            if self.rightPath >= len(rightUpgrades[self.name]):
                return 
            if app.startCash >= cost:
                self.doUpgrade(app, type, amount, cost)
                if self.rightPath < len(rightUpgrades[self.name]) - 1:
                    self.rightPath += 1

    def  doUpgradeLeft(self, app, type, amount, cost):
            if self.leftPath == len(leftUpgrades[self.name]):
                return 
            if app.startCash >= cost:
                self.doUpgrade(app, type, amount, cost)
                if self.leftPath < len(leftUpgrades[self.name]) - 1:
                    self.leftPath += 1

    def doUpgrade(self, app, type, amount, cost):
        match type:
            case 'damage':
                self.damage += amount 
            case 'pierce':
                self.pierce += amount 
            case 'range':
                self.range += amount
            case 'aps':
                self.aps += amount 
            case 'attacks':
                self.attacksPerAttack += amount 
        app.startCash -= cost 
        self.cost += cost


#------------------------------------------------------------------------------#

class UITower:
    registry = []

    def __init__(self, x, y, monkey):
        self.x = x
        self.y = y
        self.name = monkey
        self.image = tStats[monkey][4]
        self.cost = tStats[monkey][6]
        UITower.registry.append(self)
    
    def __repr__(self):
        return(f'{self.name}')

#------------------------------------------------------------------------------#



class Projectile:
    registry = []
    id = 0

    def __init__(self, startX, startY, endX, endY, monkey, bloon):
        self.startCord = (startX, startY)
        self.endCord = (endX, endY)
        self.x = startX
        self.y = startY
        Projectile.registry.append(self)
        self.id = Projectile.id
        Projectile.id += 1

        #Inherited Characteristics 
        self.timeElapsed  = 0
        self.parentTower = monkey.name
        self.damage = monkey.damage
        self.type = monkey.type
        self.bloonToHit = bloon.id
        self.hitBloon = False
        self.pierce = monkey.pierce 
        self.rotation = monkey.rotation

        #Projectile Specific Stats 
        self.lifeSpan = projStats[self.parentTower][0]
        self.speed = projStats[self.parentTower][1]

        #Traits for hitting a bloon
        self.ratePerSecond = (1/0.011)
        self.eX, self.eY = self.endCord
        self.totalDist = ((self.speed*self.ratePerSecond)*self.lifeSpan)//3 # distance = rate * time
        self.dx = self.eX - self.x
        self.dy = self.eY - self.y

    def move(self, app):
        sx, sy = self.startCord
        if self.pierce > 0:
                if self.parentTower == 'spinny':
                    self.doSpinny(sx, sy)
                else:
                    distanceToTarget = distance(self.x, self.y, *self.endCord)
                    if self.timeElapsed > self.lifeSpan:
                        Projectile.registry.remove(self)
                        return
                    
                    #Controls acceleration 
                    if distanceToTarget < self.totalDist/2:
                        dx = self.dx / 4
                        dy = self.dy / 4
                    elif distanceToTarget > self.totalDist/2:
                        dx = self.dx / 8
                        dy = self.dy / 8
                        
                    self.x += dx
                    self.y += dy
                    self.timeElapsed += .011
                for bloon in Balloon.registry:
                    if (distance(bloon.x, bloon.y, self.x, self.y) <= 20 
                        and not bloon.justHit): 
                        self.pierce -= 1
                        bloon.damage(self.damage, self.type, app)
                        self.justHit = True
                
                resetBloons()
        else:
            Projectile.registry.remove(self)
    
    #Math for the spinny tower projectile 
    def doSpinny(self, sx, sy):
        self.timeElapsed += .05
        self.x = xEquation(self.speed, self.timeElapsed) + sx
        self.y = yEquation(self.speed, self.timeElapsed) + sy

        if self.timeElapsed >= self.lifeSpan:
            Projectile.registry.remove(self)
    
#------------------------------------------------------------------------------#

class Turn:
    registry = []

    def __init__(self, x, y, radius, dir):
        self.x = x
        self.y = y
        self.d = dir
        self.radius = radius 
        Turn.registry.append(self)


