import os


def add_files_jpg(folder):
    files = os.listdir(folder)
    for file in files:
        path = os.path.join(folder, file)
        if os.path.isdir(path):
            png_folder = path.replace('\\large\\', '\\png\\')
            if not os.path.exists(png_folder):
                print('"' + path[path.rfind('\\') + 1:].lower() + '",')


add_files_jpg(r'F:\Scryfall\large')
