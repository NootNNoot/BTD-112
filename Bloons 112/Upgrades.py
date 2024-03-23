#Left and right upgrades of each tower 


#For upgrades, first number is the type of upgrade, second is the amount it 
#goes up, and the third is the cost of the upgrade 

leftUpgrades = {
    'dart':[('range', 10, 150), ('damage', 1, 300), ('attacks', 1, 450), ('damage', 1, 500), (None, None, None)],
    'bomb':[('range', 10, 250), ('damage', 1, 350), ('range', 10, 450), ('damage', 1, 650), (None, None, None)],
    'spinny':[('damage', 1, 350), ('damage', 1, 550), ('damage', 1, 750), ('damage', 2, 950), (None, None, None)],
    'ninja':[('range', 10, 210), ('pierce', 2, 350), ('attacks', 1, 500), ('attacks', 2, 850), (None, None, None)],
    'glue':[('aps', -.15, 150), ('aps', -.15, 250), ('aps', -.15, 350), ('aps', -.15, 450), (None, None, None)]
}

rightUpgrades = {
    'dart':[('pierce', 1, 200), ('aps', -.1, 300), ('pierce', 2, 500), ('aps', -.1, 650), (None, None, None)],
    'bomb':[('aps', -.15, 250), ('damage', 1, 350), ('aps', -.1, 550), ('pierce', 1, 650), (None, None, None)],
    'spinny':[('pierce', 1, 350), ('pierce', 1, 550), ('pierce', 1, 750), ('pierce', 2, 950), (None, None, None)],
    'ninja':[('damage', 1, 350), ('aps', -.15, 450), ('damage', 1, 550), ('aps', -.1, 750), (None, None, None)],
    'glue':[('damage', 1, 250), ('damage', 1, 350), ('pierce', 2, 550), ('attacks', 2, 750), (None, None, None)]
}


upgrades = {
    'dart':[leftUpgrades['dart'], rightUpgrades['dart']],
    'bomb':[leftUpgrades['bomb'], rightUpgrades['bomb']],
    'spinny':[leftUpgrades['spinny'], rightUpgrades['spinny']],
    'ninja':[leftUpgrades['ninja'], rightUpgrades['ninja']],
    'glue':[leftUpgrades['glue'], rightUpgrades['glue']]
}