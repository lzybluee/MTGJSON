import os
import re

tokens = {}
exists = []
scripts = []


def get_exists(folder):
    for pic in os.listdir(folder):
        if pic.endswith('.jpg'):
            exists.append(pic[:pic.index('.jpg')])


def get_scripts(folder):
    for script in os.listdir(folder):
        if script.endswith('.txt'):
            scripts.append(script[:script.index('.txt')])


def get_tokens(folder):
    for txt in os.listdir(folder):
        is_token = False
        code = '???'
        with open(os.path.join(folder, txt), 'r', encoding='utf8') as f:
            for line in f.readlines():
                if line.startswith('[tokens]'):
                    is_token = True
                    continue
                if is_token and line.startswith('['):
                    continue
                if line.startswith('Date='):
                    date = re.search('=(.*?)-', line).group(1)
                    if int(date) < 2007:
                        break
                if line.startswith('ScryfallCode='):
                    code = re.search('=(.*)', line).group(1)
                    if code in ['C13', 'ARC', 'FUT', 'TD2', 'VMA',
                                'ME1', 'ME2', 'ME3', 'ME4', 'PLC', 'HOP']:
                        break
                    else:
                        continue
                if is_token:
                    name = line.strip()
                    if not name or name in exists:
                        continue
                    if name in tokens:
                        tokens[name].append(code)
                    else:
                        tokens[name] = [code]


get_exists(r'F:\Scryfall\cacheDir\pics\tokens')
get_scripts(r'E:\Forge\2022\res\tokenscripts')
get_tokens(r'E:\Forge\2022\res\editions')

print(exists)
print(scripts)

for name in sorted(tokens.keys()):
    print(name, tokens[name])

for t in exists:
    if t not in scripts:
        print(t)