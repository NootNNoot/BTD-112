import math
from towerStats import *
from GameImages import monkeys 
#All stats for all projectiles 


#First is lifetime, second is speed, third is the image 
projStats = {
    'dart':[.5, 2, monkeys[1]],
    'bomb':[.25, 1.5, monkeys[3]],
    'spinny':[4*math.pi, 8, monkeys[9]],
    'ninja':[.75, 2.5, monkeys[5]],
    'glue':[.5, 1, monkeys[7]]
}