import os
import zipfile
import json

'''
’‘
'

“”
"

−–
-

[^ -~\s—•☆★ǵõäéĆâúüûêöáèñóńàíłÆ°²™®½⅓―̶…☐¡˝œ林玄泰π∞]
'''

PRINT_CHINESE = False
PRINT_CARDS = False
oracle_file = None


def write_entry(tag, content):
    if content:
        return '<{}>{}</{}>\n'.format(tag, content, tag)
    return ''


def get_card_id(card):
    if 'side' in card:
        text = card['number'] + card['side']
    else:
        text = card['number']
    text = text.replace('aa', 'a').replace('bb', 'b').replace('†', '☆')
    return text


def get_type(card):
    text = card['type'].replace('’', "'")
    if 'power' in card:
        text += ' ' + card['power'] + '/' + card['toughness']
    if 'loyalty' in card:
        text += ' (Loyalty: ' + card['loyalty'] + ')'
    return text


def get_color_indicator(card):
    text = ''
    for color in card['colorIndicator']:
        match color:
            case 'W':
                text += 'White '
            case 'U':
                text += 'Blue '
            case 'B':
                text += 'Black '
            case 'R':
                text += 'Red '
            case 'G':
                text += 'Green '
    return text.strip()


def get_rulings(card):
    text = ''
    for ruling in card['rulings']:
        text += ruling['date'].replace('-', '/') + ': ' + \
                ruling['text'].replace('’', "'").replace('‘', "'") \
                              .replace('“', '"').replace('”', '"') \
                              .replace('–', '-') + '\n'
    return text.strip()


def get_legal(card):
    if 'vintage' in card['legalities']:
        text = write_entry('Vintage', card['legalities']['vintage'])
    else:
        return ''
    text += write_entry('Legacy', card['legalities']['legacy'])
    if 'modern' in card['legalities']:
        text += write_entry('Modern', card['legalities']['modern'])
    return text


def get_watermark(card):
    text = card['watermark']
    text = text[:1].upper() + text[1:]
    match text:
        case 'Orderofthewidget':
            text = 'Order of the Widget'
        case 'Crossbreedlabs':
            text = 'Crossbreed Labs'
        case 'Leagueofdastardlydoom':
            text = 'League of Dastardly Doom'
        case 'Agentsofsneak':
            text = 'Agents of S.N.E.A.K.'
        case 'Goblinexplosioneers':
            text = 'Goblin Explosioneers'
    return text


def get_other_part(card):
    if card['name'].startswith(card['faceName'] + ' // '):
        text = card['name'].split(' // ')[1]
    else:
        text = card['name'].split(' // ')[0]

    if card['layout'] == 'split' or card['layout'] == 'aftermath':
        text += ' (' + card['name'].replace(' // ', '/') + ')'
    return text


def get_chinese_name(card):
    if 'foreignData' in card:
        for foreign_data in card['foreignData']:
            if foreign_data['language'] == 'Chinese Simplified':
                if 'faceName' in foreign_data:
                    return foreign_data['faceName']
                else:
                    return foreign_data['name']


def get_chinese_flavor(card):
    if 'foreignData' in card:
        for foreign_data in card['foreignData']:
            if foreign_data['language'] == 'Chinese Simplified':
                if 'flavorText' in foreign_data:
                    return foreign_data['flavorText']


def oracle(card, card_set):
    text = '<Card>\n'

    text += write_entry('SetId', card['setCode'] if card['setCode'] != 'CON' else 'CFX')

    card_id = get_card_id(card)
    text += write_entry('No', card_id)

    if 'faceName' in card:
        if card['layout'] == 'split' or card['layout'] == 'aftermath':
            text += write_entry('Name', card['faceName'] + ' (' + card['name'].replace(' // ', '/') + ')')
        else:
            text += write_entry('Name', card['faceName'])
    else:
        text += write_entry('Name', card['name'])

    if PRINT_CHINESE:
        text += write_entry('ChineseName', get_chinese_name(card))

    text += write_entry('Type', get_type(card))

    if 'manaCost' in card:
        text += write_entry('ManaCost', card['manaCost'])

    if 'colorIndicator' in card:
        text += write_entry('ColorIndicator', get_color_indicator(card))

    if 'text' in card:
        text += write_entry('CardText', card['text'].replace('−', '-'))

    if 'hand' in card:
        text += write_entry('HandSize', 'Hand Size: ' + card['hand'])

    if 'life' in card:
        text += write_entry('StartingLife', 'Starting Life: ' + card['life'])

    if 'flavorText' in card:
        text += write_entry('Flavor', card['flavorText'])
        if PRINT_CHINESE:
            text += write_entry('ChineseFlavor', get_chinese_flavor(card))

    if 'artist' in card:
        text += write_entry('Artist', card['artist'].replace('“', '"').replace('”', '"'))

    if 'watermark' in card:
        text += write_entry('Watermark', get_watermark(card))

    if 'multiverseId' in card['identifiers']:
        text += write_entry('Multiverseid', card['identifiers']['multiverseId'])

    if card['rulings']:
        text += write_entry('Rulings', get_rulings(card))

    if 'isReserved' in card and card['isReserved']:
        text += '<Reserved>This card is on the reserved list</Reserved>\n'

    text += get_legal(card)

    text += write_entry('Set', card_set['name'])

    text += write_entry('Rarity', card['rarity'].replace('mythic', 'mythic rare').title())

    if 'faceName' in card and ' // ' in card['name']:
        text += write_entry('OtherPart', get_other_part(card))

    text += '</Card>\n\n'

    oracle_file.write(text)

    return card_id


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
    elif number.endswith('†') or number.endswith('☆'):
        return '{:0>3}☆'.format(number[:-1])
    return '{:0>3}'.format(number)


def add_card(card_set, card, number):
    card_id = oracle(card, card_set)

    set_code = card['setCode'] if card['setCode'] != 'CON' else 'CFX'

    if not PRINT_CARDS:
        return

    pic_path = r'G:\Scryfall\png\{}\{}.png'.format(set_code, number)
    link_folder = r'F:\Scryfall\MTG\{}'.format(set_code)
    link_path = r'{}\{}.png'.format(link_folder, get_image_name(card_id))

    if number.endswith('_flip'):
        copy_folder = link_folder.replace('\\MTG', '\\MTG\\flip')
        if not os.path.exists(copy_folder):
            os.makedirs(copy_folder)
        copy_path = link_path.replace('\\MTG\\', '\\MTG\\flip\\')
        pic_path = pic_path.replace('_flip', '')
        if not os.path.exists(pic_path):
            print(':: "{}" not exist'.format(pic_path))
            return
        print('copy "{}" "{}"'.format(pic_path, copy_path))
        return
    if not os.path.exists(pic_path):
        print(':: "{}" not exist'.format(pic_path))
        return
    if not os.path.exists(link_folder):
        os.makedirs(link_folder)
    # print('mklink /h "{}" "{}"'.format(link_path, pic_path))
    print('copy "{}" "{}"'.format(pic_path, link_path))


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

    if set_code in ['FBB', 'J21', 'DBL', 'PLIST', 'MB1', '4BB', 'AJMP', 'AKR', 'ANA', 'ANB',
                    'CP1', 'CP2', 'CP3', 'FMB1', 'ITP', 'SUM', 'TSR', 'S00', 'PPOD', 'GVL', 'JVC', 'DVD',
                    'H1R', 'KLR', 'TPR', 'OANA', 'EVG', 'PUMA', 'REN', 'RIN', 'SLX', '2X2', 'PHED',
                    'DMU', 'DMC', 'CLB', 'BRO', '40K']:
        return

    if set_code == 'CON':
        set_code = 'CFX'

    global oracle_file
    oracle_file = open('Oracle/MtgOracle_' + set_code + '.txt', 'w', encoding='utf8')

    cards_json = data_json['cards']

    if output_path:
        with open(output_path, 'w', encoding='utf8') as output_file:
            output_file.write(data_json['name'] + '\n\n')
            for card_json in cards_json:
                for key, value in card_json.items():
                    if key not in ['edhrecRank', 'identifiers', 'purchaseUrls', 'legalities', 'printings']:
                        output_file.write(key + ' => ' + str(value) + '\n')
                output_file.write('\n')
    else:
        for card_json in cards_json:
            name = card_json['name']
            number = card_json['number']
            if card_json['layout'] == 'meld':
                if number.endswith('a') or number.endswith('b'):
                    add_card(set_json['data'], card_json, get_image_name(number[:-1], '', card_json['side']))
                else:
                    add_card(set_json['data'], card_json, get_image_name(number))
                continue
            if number.isdigit() and data_json['baseSetSize'] > 1:
                if int(number) > data_json['baseSetSize'] and not need_card(set_code, number):
                    continue
                if '//' in name:
                    if card_json['layout'] == 'split' or card_json['layout'] == 'aftermath':
                        add_card(set_json['data'], card_json, get_image_name(number))
                    elif card_json['layout'] == 'flip':
                        if card_json['side'] == 'a':
                            add_card(set_json['data'], card_json, get_image_name(number))
                        else:
                            add_card(set_json['data'], card_json, get_image_name(number) + '_flip')
                    elif card_json['layout'] == 'adventure':
                        add_card(set_json['data'], card_json, get_image_name(number))
                    else:
                        add_card(set_json['data'], card_json, get_image_name(number, '_', card_json['side']))
                else:
                    add_card(set_json['data'], card_json, get_image_name(number))
            elif need_card(set_code, number):
                if '//' in name:
                    add_card(set_json['data'], card_json, get_image_name(number, '_', card_json['side']))
                else:
                    add_card(set_json['data'], card_json, get_image_name(number))

    oracle_file.close()


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


load_json_from_zip(r'MTGJSON\AllSetFiles.zip', None)
