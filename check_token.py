import os
import re

tokens = {}

for file in os.listdir(r'E:\MTG\Token'):
    result = re.search(r'(.*?) ?(\d+)?\.jpg', file)
    if result:
        if result[1] in tokens:
            tokens[result[1]].append(file)
        else:
            tokens[result[1]] = [file]
    else:
        print('No match!', file)
        exit(0)

for name, pics in tokens.items():
    if len(pics) == 1:
        if pics[0] != name + '.jpg':
            print("Can't find", name + '.jpg')
            exit(0)
    elif len(pics) <= 9:
        for i in range(len(pics)):
            if '{} {}.jpg'.format(name, i + 1) not in pics:
                print("Can't find", '{} {}.jpg'.format(name, i + 1))
                exit(0)
    elif len(pics) >= 10:
        for i in range(len(pics)):
            if '{} {:02}.jpg'.format(name, i + 1) not in pics:
                print("Can't find", '{} {:02}.jpg'.format(name, i + 1))
                exit(0)
    else:
        print('len < 1!', name, pics)
        exit(0)
