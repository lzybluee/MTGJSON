import os


def find_token(folder):
    for txt in os.listdir(folder):
        with open(os.path.join(folder, txt), 'r', encoding='utf8') as f:
            token = False
            for line in f.readlines():
                if line.lower().startswith('[tokens]'):
                    token = True
                    continue
                elif line.startswith('['):
                    token = False
                if token:
                    print(line, end='')


find_token(r'E:\Forge\2021\res\editions')
