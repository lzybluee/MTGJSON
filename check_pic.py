import os


def check_pic(path):
    with open(path, 'rb') as f:
        if path.lower().endswith('.jpg'):
            f.seek(-2, os.SEEK_END)
            if f.read(2) != b'\xFF\xD9':
                print('Error', path)
        else:
            f.seek(-4, os.SEEK_END)
            if f.read(4) != b'\xAE\x42\x60\x82':
                print('Error', path)


def add_files(folder):
    files = os.listdir(folder)
    for file in files:
        path = os.path.join(folder, file)
        if os.path.isdir(path):
            print('>>>', path)
            add_files(path)
        elif path.lower().endswith('.jpg') or path.lower().endswith('.png'):
            check_pic(path)


# add_files(r'E:\MTG')
add_files(r'E:\MTG')
add_files(r'F:\Scryfall\large')
add_files(r'G:\Scryfall\png')
