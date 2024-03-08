import os
import subprocess


def check_hardlink(folder):
    files = os.listdir(folder)
    for file in files:
        path = os.path.join(folder, file)
        if os.path.isdir(path):
            check_hardlink(path)
        else:
            output = subprocess.check_output(['fsutil', 'hardlink', 'list', path]).decode('GBK')
            if r'\large' not in output:
                print(path)


check_hardlink(r'F:\Scryfall\cardPicsDir')