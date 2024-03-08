import os
import subprocess

jpg_dict = {}

for root, dirs, files in os.walk(r'F:\Scryfall\large'):
    for file in files:
        if file.endswith('.jpg'):
            size = os.path.getsize(os.path.join(root, file))
            if size in jpg_dict.keys():
                jpg_dict[size].append(os.path.join(root, file))
            else:
                jpg_dict[size] = [os.path.join(root, file)]


def check_dir(dir):
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith('.jpg'):
                result = subprocess.check_output(['fsutil', 'hardlink', 'list', os.path.join(root, file)]).decode('GBK')
                if len(result.splitlines()) == 1:
                    size = os.path.getsize(os.path.join(root, file))
                    if size in jpg_dict.keys():
                        print('del "' + os.path.join(root, file) + '"')
                        num = 0
                        for jpg in jpg_dict[size]:
                            num += 1
                            print('mklink /h "' + os.path.join(root, file) + '" "' + jpg + '"')
                        if num > 1:
                            print('===================================')
                    else:
                        print("Can't find jpg ->", os.path.join(root, file))


check_dir(r'F:\Scryfall\cardPicsDir')
check_dir(r'F:\Scryfall\cacheDir\pics\tokens')