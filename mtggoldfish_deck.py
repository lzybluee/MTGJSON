import os


def convert_deck(path, converted_path, prefix):
    print(path, '>>>', converted_path)
    with open(path, 'r') as file:
        with open(converted_path, 'w') as convert_file:
            for line in file.readlines():
                if line.startswith('Name='):
                    line = 'Name=' + prefix + ' ' + line[line.index('=') + 1:]
                convert_file.write(line)


def add_prefix(folder, prefix):
    if not os.path.exists(os.path.join('mtggoldfish', prefix)):
        os.makedirs(os.path.join('mtggoldfish', prefix))
    files = os.listdir(folder)
    for file in files:
        path = os.path.join(folder, file)
        if path.endswith('.dck'):
            converted_path = os.path.join('mtggoldfish', prefix, prefix + ' ' + file)
            convert_deck(path, converted_path, prefix)


add_prefix(r'mtggoldfish\commander_1v1', '(1v1)')
add_prefix(r'mtggoldfish\historic_brawl', '(Historic)')
