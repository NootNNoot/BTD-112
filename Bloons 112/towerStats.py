import math
import GameImages

#All tower stats 

# First value in the list is damage, second is the radius, third is the 
# time between attacks, fourth is the type of the damage, and fifth is the 
# icon of the monkey, sixth is the pierce, seventh is cost, eight is amount of 
# attacks per attack 


tStats = {
    'dart':[1, 75, .5, 'physical', GameImages.monkeys[0], 2, 210, 1],
    'bomb':[1, 50, .75, 'explosion', GameImages.monkeys[2], 1, 420, 1],
    'glue':[0, 75, 1, 'glue', GameImages.monkeys[6], 1, 210, 1],
    'spinny':[2, 63, 3.5, 'physical', GameImages.monkeys[8], 5, 750, 1],
    'ninja':[1, 95, .5, 'physical', GameImages.monkeys[4], 2, 520, 1]
}
