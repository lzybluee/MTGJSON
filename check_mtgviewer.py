import os
import re

cards = {}
oracle_num = 0
pic_num = 0

for oracle in os.listdir('Oracle'):
    set_code = oracle[oracle.index('_') + 1 : oracle.index('.')]
    cards[set_code] = []
    with open(os.path.join('Oracle', oracle), encoding='utf8') as file:
        for line in file.readlines():
            result = re.search(r'<No>(.*?)</No>', line)
            if result:
                cards[set_code].append(result.group(1))
                oracle_num += 1

print(cards)

for set_folder in os.listdir(r'F:\Scryfall\MTG'):
    for card in os.listdir(os.path.join(r'F:\Scryfall\MTG', set_folder)):
        pic_num += 1
        result = re.search(r'([^\d]*)0*(\d+)([^\d]*)', card[:card.index('.')])
        if result:
            check = result.group(1) + result.group(2) + result.group(3)
            if check not in cards[set_folder]:
                print('Not found!', set_folder, card)
        else:
            print('No number!', set_folder, card)

print(oracle_num, pic_num)