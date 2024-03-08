import os
import zipfile
import json

PRINT_SET = False
PRINT_EXIST = True
convert_map = {}


def get_forge_folder(code, number):
    if code == 'MED':
        if number.startswith('GR'):
            return 'MPS_GRN'
        if number.startswith('RA'):
            return 'MPS_RNA'
        if number.startswith('WS'):
            return 'MPS_WAR'
    if code == 'PMOA' or code == 'PVAN':
        return 'VAN'
    if code in convert_map:
        return convert_map[code]
    if code == 'PHOP' and number == 'P001':
        return 'PC2'
    if code in ['OARC', 'PARC', 'OE01', 'OHOP', 'PHOP', 'OPC2', 'OPCA']:
        return code[1:]
    return code


def get_image_name(number, concat=None, suffix=None):
    if suffix:
        return '{:0>3}{}{}'.format(number, concat, suffix)
    elif number.startswith('S') or number.startswith('P'):
        return '{}{:0>3}'.format(number[:1], number[1:])
    elif number.startswith('GP') or number.startswith('GR') or number.startswith('RA') or number.startswith('WS'):
        return '{}{:0>3}'.format(number[:2], number[2:])
    elif number.endswith('★') or number.endswith('a') or number.endswith('b') \
            or number.endswith('c') or number.endswith('d') or number.endswith('e') or number.endswith('f'):
        return '{:0>3}{}'.format(number[:-1], number[-1:])
    elif number.endswith('†'):
        return '{:0>3}☆'.format(number[:-1])
    return '{:0>3}'.format(number)


def print_card(card_set, name, number):
    if card_set == 'CON':
        card_set = 'CFX'
    if (card_set == 'UGL' and name[:-1] == 'B.F.M. (Big Furry Monster)') or \
            (card_set == 'UST' and name[:-1] in ['Knight of the Kitchen Sink', 'Very Cryptic Command',
                                                 'Sly Spy', 'Garbage Elemental', 'Ineffable Blessing',
                                                 'Everythingamajig']):
        name = name[:-1] + ' ' + chr(ord('A') + int(name[-1:]) - 1)
    pic_path = r'F:\Scryfall\large\{}\{}.jpg'.format(card_set, number)
    link_folder = r'F:\Scryfall\cardPicsDir\{}'.format(get_forge_folder(card_set, number))
    link_path = r'{}\{}.full.jpg'.format(link_folder, name.replace(':', '').replace('"', '').replace('?', '')
                                         .replace('á', 'a').replace('ú', 'u').replace('û', 'u').replace('é', 'e')
                                         .replace('à', 'a').replace('ö', 'o').replace('í', 'i').replace('â', 'a')
                                         .replace('®', '').replace(' . . .', '...'))
    if number.endswith('_flip'):
        copy_folder = link_folder.replace('\\cardPicsDir', '\\cardPicsDir\\flip')
        if not os.path.exists(copy_folder):
            os.makedirs(copy_folder)
        copy_path = link_path.replace('\\cardPicsDir\\', '\\cardPicsDir\\flip\\')
        pic_path = pic_path.replace('_flip', '')
        if not os.path.exists(pic_path):
            print(':: "{}" not exist'.format(pic_path))
            return
        if not os.path.exists(link_path) or PRINT_EXIST:
            print('copy "{}" "{}"'.format(pic_path, copy_path))
        return
    if not os.path.exists(pic_path):
        print(':: "{}" not exist'.format(pic_path))
        return
    if not os.path.exists(link_folder):
        os.makedirs(link_folder)
    if not os.path.exists(link_path) or PRINT_EXIST:
        print('mklink /h "{}" "{}"'.format(link_path, pic_path))


def need_card(card_set, number):
    if number.isdigit():
        number = int(number)
        if card_set == 'ELD':
            return 303 <= number <= 333
        elif card_set == 'THB':
            return 269 <= number <= 297
        elif card_set == 'IKO':
            return number == 275
        elif card_set == 'M21':
            return number == 278 or 309 <= number <= 313 or 320 <= number <= 339
        elif card_set == 'CMR':
            return 362 <= number <= 511 or number == 721
        elif card_set == 'KHM':
            return 374 <= number <= 398
        elif card_set == 'KHC':
            return 1 <= number <= 16
        elif card_set == 'ZNC':
            return 1 <= number <= 6
        elif card_set == 'STX':
            return 366 <= number <= 375
        elif card_set == 'ZNR':
            return 380 <= number <= 384
        elif card_set == 'MID':
            return 380 <= number <= 384
        elif card_set == 'VOW':
            return 398 <= number <= 402
        elif card_set == 'AKH':
            return 270 <= number <= 287
        elif card_set == 'BBD':
            return 255 <= number <= 256
        elif card_set == 'CN2':
            return number == 222
        elif card_set == 'DOM':
            return 270 <= number <= 280
        elif card_set == 'GRN':
            return 260 <= number <= 273
        elif card_set == 'HOU':
            return 200 <= number <= 209
        elif card_set == 'KLD':
            return 265 <= number <= 274
        elif card_set == 'M15':
            return 270 <= number <= 284
        elif card_set == 'M19':
            return 281 <= number <= 314
        elif card_set == 'M20':
            return 281 <= number <= 344
        elif card_set == 'MH1':
            return number == 255
        elif card_set == 'MH2':
            return 481 <= number <= 491
        elif card_set == 'ORI':
            return 273 <= number <= 288
        elif card_set == 'AER':
            return 185 <= number <= 194
        elif card_set == 'RIX':
            return 197 <= number <= 205
        elif card_set == 'RNA':
            return 260 <= number <= 273
        elif card_set == 'WAR':
            return 265 <= number <= 275
        elif card_set == 'XLN':
            return 280 <= number <= 289
        elif card_set == 'SLD':
            return 143 <= number <= 147 or 340 <= number <= 347 or number == 609
        elif card_set == 'UNH':
            return number == 141
        elif card_set == 'PARC':
            return 54 <= number <= 58
        elif card_set == 'PHOP':
            return 41 <= number <= 45
        elif card_set == 'HHO':
            return 18 <= number <= 21
        elif card_set == 'PVAN' or card_set == 'PMOA':
            return True
    elif card_set == '8ED' or card_set == '9ED':
        return number.startswith('S')
    elif card_set == 'G18':
        return number.startswith('GP')
    elif card_set == 'ATQ':
        return number.endswith('a') or number.endswith('b') or number.endswith('c') or number.endswith('d')
    elif card_set in ['ALL', 'CHK', 'HML', 'FEM', 'BFZ', 'ME4', 'ARN', 'PLS', 'POR', 'CHR']:
        return number.endswith('†') or number.endswith('a') or number.endswith('b') or \
               number.endswith('c') or number.endswith('d') or number.endswith('★')
    elif card_set == 'UST':
        return number.endswith('a') or number.endswith('b') or number.endswith('c') or \
               number.endswith('d') or number.endswith('e') or number.endswith('f')
    elif card_set == 'BFZ' or card_set == 'OGW' or card_set == 'ZEN':
        return number.endswith('a')
    elif card_set == 'OARC' or card_set == 'OE01':
        return number.endswith('★')
    elif card_set == 'PHOP':
        return number == 'P1'
    elif card_set == 'MED':
        return number.startswith('GR') or number.startswith('RA') or number.startswith('WS')


def add_card(cards_map, name, number):
    if name in cards_map:
        cards_map[name].append(number)
    else:
        cards_map[name] = [number]


def load_set(set_data, output_path):
    set_json = json.loads(set_data)
    data_json = set_json['data']
    set_code = data_json['code']

    if data_json['type'] not in ['core', 'expansion', 'commander', 'draft_innovation', 'planechase', 'archenemy',
                                 'starter', 'masters', 'masterpiece', 'duel_deck', 'from_the_vault', 'premium_deck'] \
            and set_code not in ['E02', 'CM1', 'G18', 'GK1', 'GK2', 'GN2', 'GNT', 'UGL', 'UND', 'UNH', 'UST',
                                 'CMB1', 'HTR16', 'HTR17', 'HTR18', 'HTR19', 'HHO', 'SLD', 'PHOP', 'PMOA', 'PVAN']:
        # 'vanguard', 'funny'
        # 'promo', 'box', 'memorabilia', 'token', 'arsenal', 'spellbook', 'treasure_chest', 'alchemy'
        return

    if set_code in ['FBB', 'CLB', 'J21', 'DBL', 'PLIST', 'MB1', '4BB', 'AJMP', 'AKR', 'ANA', 'ANB',
                    'CP1', 'CP2', 'CP3', 'FMB1', 'ITP', 'SUM', 'TSR', 'S00', 'PPOD', 'GVL', 'JVC', 'DVD',
                    'H1R', 'KLR', 'TPR', 'OANA', 'EVG', 'PUMA', 'REN', 'RIN', '2X2', '40K', 'PHED', 'SLX']:
        return

    if PRINT_SET:
        cards_json = data_json['cards'] + data_json['tokens']
    else:
        cards_json = data_json['cards']

    cards_map = {}

    if output_path:
        with open(output_path, 'w', encoding='utf8') as output_file:
            output_file.write(data_json['name'] + '\n\n')
            for card_json in cards_json:
                for key, value in card_json.items():
                    if key not in ['edhrecRank', 'identifiers', 'purchaseUrls', 'legalities', 'printings']:
                        output_file.write(key + ' => ' + str(value) + '\n')
                output_file.write('\n')
    else:
        if PRINT_SET:
            print(data_json['name'] + '\n')
            for card_json in cards_json:
                for key, value in card_json.items():
                    if key not in ['edhrecRank', 'identifiers', 'purchaseUrls', 'legalities', 'printings']:
                        print(key, '=>', value)
            print()
        else:
            for card_json in cards_json:
                name = card_json['name']
                number = card_json['number']
                if card_json['layout'] == 'meld':
                    if number.endswith('a') or number.endswith('b'):
                        add_card(cards_map, card_json['faceName'], get_image_name(number[:-1], '', card_json['side']))
                    else:
                        add_card(cards_map, card_json['faceName'], get_image_name(number))
                    continue
                if number.isdigit() and data_json['baseSetSize'] > 1:
                    if int(number) > data_json['baseSetSize'] and not need_card(set_code, number):
                        continue
                    if '//' in name:
                        if card_json['layout'] == 'split' or card_json['layout'] == 'aftermath':
                            if name.startswith(card_json['faceName']):
                                add_card(cards_map, name.replace(' // ', ''), get_image_name(number))
                        elif card_json['layout'] == 'flip':
                            if card_json['side'] == 'a':
                                add_card(cards_map, card_json['faceName'], get_image_name(number))
                            else:
                                add_card(cards_map, card_json['faceName'], get_image_name(number) + '_flip')
                        elif card_json['layout'] == 'adventure':
                            add_card(cards_map, card_json['faceName'], get_image_name(number))
                        else:
                            add_card(cards_map, card_json['faceName'], get_image_name(number, '_', card_json['side']))
                    else:
                        add_card(cards_map, name, get_image_name(number))
                elif need_card(set_code, number):
                    if '//' in name:
                        add_card(cards_map, card_json['faceName'], get_image_name(number, '_', card_json['side']))
                    else:
                        add_card(cards_map, name, get_image_name(number))

    for name, cards in cards_map.items():
        if len(cards) == 1:
            print_card(set_code, name, cards[0])
        else:
            for i in range(len(cards)):
                print_card(set_code, name + str(i + 1), cards[i])


def load_json(json_path, output_path=None):
    with open(json_path, 'r', encoding='utf8') as json_file:
        load_set(json_file.read(), output_path)


def load_json_from_zip(zip_path, file_path, output_path=None):
    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        for file_name in sorted(zip_file.namelist()):
            if not file_path or file_name == file_path:
                json_file = zip_file.open(file_name)
                load_set(json_file.read(), output_path)
                json_file.close()


def load_all_from_zip(zip_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        for file_name in sorted(zip_file.namelist()):
            print(file_name)
            json_file = zip_file.open(file_name)
            load_set(json_file.read(), os.path.join(output_folder, file_name.replace('.json', '.txt')))
            json_file.close()


def generate_forge(folder):
    for txt in os.listdir(folder):
        with open(os.path.join(folder, txt), 'r', encoding='utf8') as f:
            scryfall_code = None
            forge_code2 = None
            for line in f.readlines():
                if line.startswith('Code='):
                    forge_code = line[line.find('=') + 1:-1].upper()
                if line.startswith('Code2='):
                    forge_code2 = line[line.find('=') + 1:-1].upper()
                if line.startswith('ScryfallCode='):
                    scryfall_code = line[line.find('=') + 1:-1].upper()
                if line.startswith('[') and 'metadata' not in line:
                    break
            if scryfall_code:
                if forge_code2:
                    convert_map[scryfall_code] = forge_code2
                elif forge_code:
                    convert_map[scryfall_code] = forge_code


generate_forge(r'E:\Forge\2022\res\editions')
load_json_from_zip(r'MTGJSON\AllSetFiles.zip', None)
