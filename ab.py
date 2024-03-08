import os

def add_files_jpg(folder):
    files = os.listdir(folder)
    for file in files:
        path = os.path.join(folder, file)
        if os.path.isdir(path):
            add_files_jpg(path)
        else:
            if file.endswith('a.jpg') and not os.path.exists(path.replace('a.jpg', 'b.jpg')):
                print(path)
            if file.endswith('b.jpg') and not os.path.exists(path.replace('b.jpg', 'a.jpg')):
                print(path)


add_files_jpg(r'E:\MTG')