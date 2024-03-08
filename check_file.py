import os


def check_png(png):
    jpg = png.replace('\\png\\', '\\large\\').replace('.png', '.jpg').replace('G:', 'F:')
    if not os.path.exists(jpg):
        print('No corresponding JPG:', png)


def add_files_png(folder):
    files = os.listdir(folder)
    for file in files:
        path = os.path.join(folder, file)
        if os.path.isdir(path):
            add_files_png(path)
        else:
            check_png(path)


add_files_png(r'G:\Scryfall\png')

print('===============================')


def check_jpg(jpg):
    png = jpg.replace('\\large\\', '\\png\\').replace('.jpg', '.png').replace('F:', 'G:')
    if not os.path.exists(png):
        print('No corresponding PNG:', jpg)


def add_files_jpg(folder):
    files = os.listdir(folder)
    for file in files:
        path = os.path.join(folder, file)
        if os.path.isdir(path):
            add_files_jpg(path)
        else:
            check_jpg(path)


add_files_jpg(r'F:\Scryfall\large')
