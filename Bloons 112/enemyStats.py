from ChildrenDict import *
from GameImages import *
import random

#Has bloon resistances, stats, the list of waves, and the function to make 
#random waves

resistances = {
    'red':[],
    'blue':[],
    'green':[],
    'yellow':[],
    'pink':[],
    'black':['explosion'],
    'white':['glue'],
    'lead':['physical', 'freeze'],
    'zebra':['glue', 'explosion'],
    'rainbow':[]
}

# First value in the list is the health, the second is the speed, the third is 
# the image of the bloon, fourth is the Children of the Bloon, fifth is 
# the bloons resistances, the sixth is a tag if a bloon is a "special" 
# bloon(contains children). 

eStats = {
    1:[1, 1.2, bloonImages[0], children['red'], resistances['red'], 1],
    2:[2, 1.3, bloonImages[1], children['blue'], resistances['blue'], ],
    3:[3, 1.5, bloonImages[2], children['green'], resistances['green']], 
    4:[4, 2.5, bloonImages[3], children['yellow'], resistances['yellow']], 
    5:[5, 3.5, bloonImages[4], children['pink'], resistances['pink']], 
    6:[6, 1.8, bloonImages[5], children['black'], resistances['black'], 'special'],
    7:[6, 2, bloonImages[6], children['white'], resistances['white'], 'special'],
    8:[7, 1.3, bloonImages[7], children['lead'], resistances['lead'], 'special'], #lead bloon
    9:[8, 1.6, bloonImages[8], children['zebra'], resistances['zebra'], 'special'], #zebra bloon
    10:[9, 2.3, bloonImages[9], children['rainbow'], resistances['rainbow'], 'special'] #rainbow bloon 

}

#All the predetermined waves 
bloonList = {
    1:[1 for i in range((20))], 
    2:[1 for i in range(30)],
    3:[1 for i in range(20)] + [2 for i in range(5)],
    4:[1 for i in range(30)] + [2 for i in range(15)],
    5:[1 for i in range(5)] + [2 for i in range(25)],
    6:[1 for i in range(15)] + [2 for i in range(15)] + [3 for i in range(4)],
    7:[1 for i in range(20)] + [2 for i in range(25)] + [3 for i in range(5)],
    8:[1 for i in range(10)] + [2 for i in range(20)] + [3 for i in range(14)],
    9:[3 for i in range(30)],
    10:[2 for i in range(45)],
    11:[1 for i in range(10)] + [2 for i in range(10)] + [3 for i in range(12)] + [4 for i in range(2)],
    12:[2 for i in range(15)] + [3 for i in range(10)] + [4 for i in range(5)],
    13:[1 for i in range(30)] + [3 for i in range(20)] + [4 for i in range(4)],
    14:[1 for i in range(30)] + [2 for i in range(10)] + [3 for i in range(10)] + [4 for i in range(9)],
    15:[1 for i in range(20)] + [3 for i in range(12)] + [4 for i in range(5)] + [5 for i in range(3)],
    16:[3 for i in range(20)] + [4 for i in range(8)] + [5 for i in range(4)],
    17:[6 for i in range(6)],
    18:[5 for i in range(15)],
    19:[7 for i in range(8)],
    20:[6 for i in range(5)] + [7 for i in range(4)],
    21:[4 for i in range(31)],
    22:[5 for i in range(23)] + [9 for i in range(4)],
    23:[8 for i in range(4)],
    24:[9 for i in range(8)] + [8 for i in range(2)],
    25:[8 for i in range(9)],
    26:[6 for i in range(25)] + [7 for i in range(28)] + [8 for i in range(8)],
    27:[4 for i in range(60)] + [9 for i in range(5)],
    28:[5 for i in range(35)] + [7 for i in range(25)] + [10 for i in range(5)]
}
