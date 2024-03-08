import os
import zipfile
import json
import re


emblem_pic = []
emblem_txt = []


def load_set(set_data):
    set_json = json.loads(set_data)
    data_json = set_json['data']
    set_code = data_json['code']
    cards_json = data_json['tokens']

    for card_json in cards_json:
        name = card_json['name']
        number = card_json['number']
        if card_json['type'].startswith("Emblem"):
            if set_code == 'MED' or set_code == 'NEO' or set_code == 'VOW':
                continue
            if name == 'Daretti, Scrap Savant Emblem' and set_code != 'CM2':
                continue
            if name == 'Ob Nixilis Reignited Emblem' and set_code != 'C19':
                continue
            if name == 'Dack Fayden Emblem' and set_code != 'EMA':
                continue
            if name == 'Liliana of the Dark Realms Emblem' and set_code != 'M14':
                continue
            if name == 'Elspeth, Knight-Errant Emblem' and set_code != 'MMA':
                continue
            if name == 'Domri Rade Emblem' and set_code != 'MM3':
                continue
            if name == 'Arlinn Kord Emblem':
                name = 'Arlinn, Embraced by the Moon Emblem'
            jpg = 'F:\\Scryfall\\large\\' + 'T' + set_code + '\\{:0>3}'.format(number) + '.jpg'
            if not os.path.exists(jpg):
                print('Not exist', '=>', jpg)
            name = 'emblem_' + \
                   name.replace(' Emblem', '').lower()\
                .replace(',', '').replace("'", '').replace(' ', '_').replace('-', '_')
            token = 'F:\\Scryfall\\cacheDir\\pics\\tokens\\' + name + '.jpg'
            emblem_pic.append(name)
            print('mklink /h "' + token + '" "' + jpg + '"')


def load_json(json_path):
    with open(json_path, 'r', encoding='utf8') as json_file:
        load_set(json_file.read())


def load_json_from_zip(zip_path, file_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        for file_name in sorted(zip_file.namelist()):
            if not file_path or file_name == file_path:
                json_file = zip_file.open(file_name)
                load_set(json_file.read())
                json_file.close()


def get_forge_cards():
    with zipfile.ZipFile(r'E:\Forge\2021\res\cardsfolder\cardsfolder.zip', 'r') as zip_file:
        for name in zip_file.namelist():
            if name.lower().endswith('.txt'):
                file = zip_file.open(name)
                card_text = file.read().decode('utf-8')
                result = re.search(r'(emblem_[\w_]+)', card_text)
                if result:
                    emblem_txt.append(result.group(1))
                else:
                    result = re.search(r'Name\$ (Emblem [^|]+)', card_text)
                    if result:
                        emblem = result.group(1).strip().lower().replace(' - ', ' ')\
                            .replace(',', '').replace("'", '').replace(' ', '_').replace('-', '_')
                        emblem_txt.append(emblem)
                file.close()


get_forge_cards()
load_json_from_zip(r'D:\Develop\Python\Projects\json\MTGJSON\AllSetFiles.zip', None)

for emblem in emblem_pic:
    if emblem not in emblem_txt:
        print(emblem)

print('=' * 20)

for emblem in emblem_txt:
    if emblem not in emblem_pic:
        print(emblem)
