from cmu_graphics import *
from PIL import *
import os, pathlib
#All images that appear in the game 



#Citation: This function was taken basically straigt from the basicPILMethods 
#file provided to us in piazza (Piazza post @2147)

def createImage(imagePath):
    image = Image.open(os.path.join(pathlib.Path(__file__).parent,imagePath))
    return CMUImage(image)


#Citation: All images have been exclusively captured from the actual game of BTD 5, 
#where all credit goes to NinjaKiwi, publisher of the game or from the Bloons
# Wiki which you can find here: https://bloons.fandom.com/wiki/Bloons_Wiki
images = [
    createImage(r'GameUI\BTD5startScreen.png'), 
    createImage(r"GameUI\Easy Map.png"), 
    createImage(r"MapSelectorUI\RightArrow.png"), 
    createImage(r"MapSelectorUI\LeftArrow2.png"), 
    createImage(r'MapSelectorUI\playButton.png'),
    createImage(r'GameUI\upgradeBackground.png'),
    createImage(r'BloonImages\selectBackground.png')
]

bloonImages = [
    createImage(r'BloonImages\redBloon.png'), 
    createImage(r'BloonImages\blueBloon.png'),
    createImage(r'BloonImages\greenBloon.png'),
    createImage(r'BloonImages\yellowBloon.png'),
    createImage(r'BloonImages\pinkBloon.png'),
    createImage(r'BloonImages\blackBloon.png'),
    createImage(r'BloonImages\whiteBloon.png'),
    createImage(r'BloonImages\leadBloon.png'),
    createImage(r'BloonImages\zebraBloon.png'),
    createImage(r'BloonImages\rainbowBloon.png')

]

gameIcons = [
    createImage(r'GameUI\dartMonkey.jpg'),
    [createImage(r'GameUI\Easy Map.png'), createImage(r'GameUI\Medium Map.png'),
     createImage(r'GameUI\Hard Map.png')],
    createImage(r'GameUI\gGunner.png'),
    createImage(r'GameUI\bTower.png'),
    createImage(r'GameUI\ninja.png'),
    createImage(r'GameUI\spinny.png')
]

monkeys = [
    createImage(r'MonkeyImages\dartMonkey.png'),
    createImage(r'MonkeyImages\dartDart.png'),
    createImage(r'MonkeyImages\bombTower.png'),
    createImage(r'MonkeyImages\bombBomb.png'),
    createImage(r"MonkeyImages\ninjaMonkey.png"),
    createImage(r'MonkeyImages\ninjaShuriken.png'),
    createImage(r'MonkeyImages\glueGunner.png'),
    createImage(r'MonkeyImages\glueGlue.png'),
    createImage(r'MonkeyImages\spinnyMonkeyy.png'),
    createImage(r'MonkeyImages\spinnySaw.png')
]