import re

# TOME_FILE = 'Tome/MtgTome_8E.txt'
# ORACLE_FILE = 'Chinese_Oracle/MtgOracle_8ED.txt'

TOME_FILE = 'Tome/MtgTome_MI.txt'
ORACLE_FILE = 'Chinese_Oracle/MtgOracle_MRD.txt'


def update_card(card, chinese_dict):
    name = re.findall('<Name>(.*)</Name>', card)[0]
    if name not in chinese_dict:
        print(card)
        exit(1)
    else:
        multiverse_id = re.findall('<Multiverseid>(.*)</Multiverseid>', card)[0]
        flavor = re.findall('<Flavor>(.*)</Flavor>', card, re.DOTALL)
        print(multiverse_id)
        print(name)
        print(chinese_dict[name][0])
        if flavor:
            print(flavor[0])
            if chinese_dict[name][1]:
                print('--------')
                print(chinese_dict[name][1])
            else:
                print('???')
        print()


def main():
    chinese_dict = {}
    with open(TOME_FILE, encoding='utf8') as file:
        name = ''
        chinese_name = ''
        flavor = ''
        chinese_flavor = ''
        for line in file.readlines():
            line = line.strip()
            if not line:
                chinese_dict[name] = [chinese_name, chinese_flavor.strip()]
                name = ''
                chinese_name = ''
                flavor = ''
                chinese_flavor = ''
                continue
            elif not name:
                name = line
                continue
            elif not chinese_name:
                chinese_name = line
                continue
            elif re.findall('[a-zA-Z]', line):
                flavor += line + '\n'
            else:
                chinese_flavor += line + '\n'

    # print(chinese_dict)

    with open(ORACLE_FILE, encoding='utf8') as file:
        card = ''
        for line in file.readlines():
            line = line.strip()
            if not line:
                update_card(card, chinese_dict)
                card = ''
            else:
                card += line + '\n'

    print('========')


main()