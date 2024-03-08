import os
import re

CHECK_SHEET = False
CHECK_NO_BASIC = False


def forge(folder):
    sheets = {}
    from_sheets = {}
    for txt in os.listdir(folder):
        with open(os.path.join(folder, txt), 'r', encoding='utf8') as f:
            set_code = None
            forge_code2 = None
            forge_code = None
            cards = {}
            flag = False
            sections = []
            need_sheets = []
            set_type = ''
            for line in f.readlines():
                if line.startswith('['):
                    sections.append(line.strip()[1:-1])
                if 'fromSheet' in line:
                    for sheet in re.findall(r'fromSheet\(["\'](.*?)["\']\)', line):
                        need_sheets.append(sheet)
                if line.startswith('Type='):
                    set_type = line[line.find('=') + 1:-1].lower()
                    continue
                if line.startswith('Code='):
                    forge_code = line[line.find('=') + 1:-1].upper()
                    continue
                if line.startswith('Code2='):
                    forge_code2 = line[line.find('=') + 1:-1].upper()
                    continue
                if line.startswith("[cards]"):
                    flag = True
                    continue
                if flag and (line.startswith("[")):
                    if not line.startswith('[buy a box]') and not line.startswith('[precon product]') \
                            and not line.startswith('[dungeons]') and not line.startswith('[special slot]'):
                        flag = False
                    continue
                if flag:
                    result = re.search(r'^(\S+\s+)?[A-Z]+\s+([^@]+)', line)
                    if result:
                        card = result.group(2).strip()\
                            .replace(' // ', '').replace(':', '').replace('"', '').replace('?', '')
                        if card not in cards:
                            cards[card] = 1
                        else:
                            cards[card] += 1
                    elif line.strip():
                        print(txt, line)
            if forge_code2:
                set_code = forge_code2
            elif forge_code:
                set_code = forge_code

            if not cards:
                print(txt, 'No cards!')

            pic_dir = 'F:\\Scryfall\\cardPicsDir\\'
            for card, num in cards.items():
                if num == 1:
                    if not os.path.exists(pic_dir + set_code + '\\' + card + '.full.jpg'):
                        print(txt, set_code, card)
                else:
                    for i in range(1, num + 1):
                        if not os.path.exists(pic_dir + set_code + '\\' + card + str(i) + '.full.jpg'):
                            print(txt, set_code, card, num)

            if CHECK_NO_BASIC and set_type in ['core', 'expansion', 'draft']:
                if 'Forest' not in cards:
                    print(txt, set_code, 'No basic lands!')

            sheets[set_code] = sections
            if need_sheets:
                from_sheets[set_code] = need_sheets

    if CHECK_SHEET:
        for set_code, sections in from_sheets.items():
            for section in sections:
                need_set = section[:section.index(' ')]
                need_section = section[section.index(' ') + 1:]
                if need_set not in sheets:
                    print(set_code, "Can't find need_set", need_set)
                elif need_section not in sheets[need_set]:
                    print(set_code, 'needs', need_set, need_section)


forge(r'E:\Forge\2021\res\editions')
