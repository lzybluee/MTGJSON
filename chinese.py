import os
import re
import time
import requests
import threading


TEST = False
SKIP_EXIST = True
MAX_THREADS = 16
threads = 0


def get_url(url):
    while True:
        try:
            requests.packages.urllib3.disable_warnings()
            respond = requests.get(url, verify=False, timeout=30)
            break
        except Exception as e:
            print('Get URL exception', url, e)
            time.sleep(60)
    return respond.text


def get_entry(page, entry, multiverse_id):
    results = re.findall(entry + ':</div>(.*?)</div>', page, re.DOTALL)
    if not results:
        return
    for result in results:
        result = result.replace('&lt;', '<').replace('&gt;', '>')
        text = re.sub('<[^>]+>', '', result).strip()
        if text:
            return text
        else:
            print("Can't find entry!", multiverse_id, entry)
            exit(1)


def get_flavor(page, entry, multiverse_id):
    results = re.findall(entry + ':</div>(.*?)<div class="label">', page, re.DOTALL)
    if not results:
        return
    for result in results:
        result = result.replace('&lt;', '<').replace('&gt;', '>').replace("</div><div class='flavortextbox'>", '\n')
        text = re.sub('<[^>]+>', '', result).strip()
        text = text.replace('\r\n', '\n').replace('\r', '\n').replace('」～', '」\n～')
        while '\n\n' in text:
            text = text.replace('\n\n', '\n')
        if text:
            return text
        else:
            print("Can't find entry!", multiverse_id, entry)
            exit(1)


def get_page_name(page):
    results = re.findall('<span id="ctl00_ctl00_ctl00_MainContent_SubContent_SubContentHeader_subtitleDisplay"[^>]*>(.*?)</span>', page)
    return results[0]


def get_card_info(multiverse_id):
    page = get_url('https://gatherer.wizards.com/Pages/Card/Details.aspx?printed=true&multiverseid=' + multiverse_id)
    if '<!-- End Card Details Table -->' in page:
        page_name = get_page_name(page)
        name = get_entry(page, 'Card Name', multiverse_id)
        card_set = get_entry(page, 'Expansion', multiverse_id)
        page_parts = page.split('<!-- End Card Details Table -->')
        if '//' in page_name:
            name = page_name
            flavor = None
            card_set = get_entry(page_parts[0], 'Expansion', multiverse_id)
            number = get_entry(page_parts[0], 'Card Number', multiverse_id)
        elif card_set in ['Throne of Eldraine', 'Champions of Kamigawa', 'Betrayers of Kamigawa', 'Saviors of Kamigawa',
                          'Magic: The Gathering-Commander', 'Commander 2018', 'Commander Anthology 2018']:
            name = name + ' // ' + get_entry(page_parts[1], 'Card Name', multiverse_id)
            flavor = get_flavor(page_parts[0], 'Flavor Text', multiverse_id)
            number = get_entry(page_parts[0], 'Card Number', multiverse_id)
        else:
            if name == page_name:
                flavor = get_flavor(page_parts[0], 'Flavor Text', multiverse_id)
                card_set = get_entry(page_parts[0], 'Expansion', multiverse_id)
                number = get_entry(page_parts[0], 'Card Number', multiverse_id)
            else:
                name = get_entry(page_parts[1], 'Card Name', multiverse_id)
                flavor = get_flavor(page_parts[1], 'Flavor Text', multiverse_id)
                card_set = get_entry(page_parts[1], 'Expansion', multiverse_id)
                number = get_entry(page_parts[1], 'Card Number', multiverse_id)
    else:
        name = get_entry(page, 'Card Name', multiverse_id)
        flavor = get_flavor(page, 'Flavor Text', multiverse_id)
        card_set = get_entry(page, 'Expansion', multiverse_id)
        number = get_entry(page, 'Card Number', multiverse_id)

    if TEST:
        print(multiverse_id, ';', name, ';', flavor, ';', card_set, ';', number)
    return name, flavor, card_set, number


def get_chinese_card(multiverse_id, card_set, number):
    language_page = get_url('https://gatherer.wizards.com/Pages/Card/Languages.aspx?multiverseid=' + multiverse_id)
    page_index = 1
    while True:
        if '/Pages/Card/Languages.aspx?page=' + str(page_index) + '&' in language_page:
            language_page += get_url('https://gatherer.wizards.com/Pages/Card/Languages.aspx?page=' + str(page_index) + '&multiverseid=' + multiverse_id)
            page_index += 1
        else:
            break
    if 'No printings of this card in other languages are available at this time' in language_page:
        return '???', '???'
    results = re.findall('<tr class="cardItem (even|odd)Item">(.*?)</tr>', language_page, re.DOTALL)
    for result in results:
        if 'Chinese Simplified' in result[1]:
            chinese_ids = re.findall(r'multiverseid=(\d+)', result[1], re.DOTALL)
            name, flavor, chinese_set, chinese_number = get_card_info(chinese_ids[0])
            if chinese_set == card_set and chinese_number == number:
                return name, flavor
    return None, None


def get_chinese(multiverse_id):
    english_name, english_flavor, card_set, number = get_card_info(multiverse_id)
    chinese_name, chinese_flavor = get_chinese_card(multiverse_id, card_set, number)
    return english_name, chinese_name, english_flavor, chinese_flavor


def process_oracle(oracle, file_name, chinese_file):
    oracle_num = 0
    chinese_num = 0
    no_chinese_num = 0
    with open(chinese_file, 'w', encoding='utf8') as chinese:
        with open(oracle, encoding='utf8') as file:
            for line in file.readlines():
                if line.startswith('<Multiverseid>'):
                    oracle_num += 1
                    multiverse_id = re.sub('<[^>]+>', '', line).strip()
                    retry = 0
                    while retry < 10:
                        english_name, chinese_name, english_flavor, chinese_flavor = get_chinese(multiverse_id)
                        if chinese_name:
                            if chinese_name == '???':
                                no_chinese_num += 1
                            else:
                                chinese_num += 1
                            chinese.write(multiverse_id + '\n')
                            if english_name:
                                chinese.write(english_name + '\n')
                            else:
                                chinese.write('???\n')
                            chinese.write(chinese_name + '\n')
                            if english_flavor:
                                chinese.write(english_flavor + '\n')
                            if english_flavor and chinese_flavor:
                                chinese.write('--------\n')
                            if chinese_flavor:
                                chinese.write(chinese_flavor + '\n')
                            chinese.write('\n')
                            chinese.flush()
                            if retry > 8:
                                print("Retry find chinese!", file_name, multiverse_id)
                            break
                        elif chinese_num > 0:
                            if retry >= 8:
                                print("Can't find chinese!", file_name, multiverse_id, retry)
                            time.sleep(10)
                            retry += 1
                        else:
                            break

                    if no_chinese_num > 3 and chinese_num == 0:
                        chinese.truncate(0)
                        break

        if chinese_num > 0:
            chinese.write('========')

    if chinese_num > 0 and chinese_num != oracle_num:
        print('Number mismatch!', file_name, oracle_num, chinese_num, no_chinese_num)
    else:
        print('Finished!', file_name, oracle_num, chinese_num, no_chinese_num)

    global threads
    threads -= 1


def update_card(card, chinese_dict):
    multiverse_id = re.findall('<Multiverseid>(.*)</Multiverseid>', card)
    if multiverse_id and multiverse_id[0] in chinese_dict:
        chinese = chinese_dict[multiverse_id[0]]
        card = card.replace('</Name>', '</Name>\n<ChineseName>' + chinese[1] + '</ChineseName>')
        if len(chinese) > 3:
            card = card.replace('</Flavor>', '</Flavor>\n<ChineseFlavor>' + chinese[3] + '</ChineseFlavor>')
    if '<Name>+2 Mace</Name>' in card:
        card = card.replace('</Name>', '</Name>\n<ChineseName>+2硬头锤</ChineseName>')
        card = card.replace('</Flavor>', '</Flavor>\n<ChineseFlavor>这件魔法武器对恶人砸得特别重。</ChineseFlavor>')
    return card


def process_update(oracle, file_name):
    print('Update', oracle)

    chinese_dict = {}
    with open(os.path.join('Chinese', file_name), encoding='utf8') as chinese:
        multiverse_id, english_name, chinese_name, english_flavor, chinese_flavor = None, None, None, None, None
        for line in chinese.readlines():
            line = line.strip()
            if not line:
                if english_flavor and not chinese_flavor:
                    print('No chinese flavor', file_name, multiverse_id)
                    exit(1)
                if re.findall('[a-zA-Z]', chinese_name):
                    print('Found english in chinese name', oracle, multiverse_id, chinese_name)
                if chinese_flavor:
                    # if re.findall('[a-zA-Z]', chinese_flavor):
                    #     print('Found english in chinese flavor', oracle, multiverse_id, chinese_flavor)
                    chinese_dict[multiverse_id] = [english_name, chinese_name, english_flavor.strip(), chinese_flavor.strip()]
                else:
                    chinese_dict[multiverse_id] = [english_name, chinese_name]
                multiverse_id, english_name, chinese_name, english_flavor, chinese_flavor = None, None, None, None, None
                continue
            if not multiverse_id:
                multiverse_id = line
                continue
            if not english_name:
                english_name = line
                continue
            if not chinese_name:
                chinese_name = line
                english_flavor = ''
                continue
            if chinese_flavor is not None:
                chinese_flavor += line + '\n'
                continue
            if line == '--------':
                chinese_flavor = ''
                continue
            if english_flavor is not None:
                english_flavor += line + '\n'
                continue
            if line == '========':
                break

    with open(os.path.join('Chinese_Oracle', file_name), 'w', encoding='utf8') as chinese_oracle:
        with open(oracle, encoding='utf8') as oracle:
            card = ''
            for line in oracle.readlines():
                line = line.strip()
                if not line:
                    chinese_oracle.write(update_card(card, chinese_dict) + '\n')
                    card = ''
                    continue
                card += line + '\n'


def update():
    folder = r'E:\MTG\Oracle'
    files = os.listdir(folder)
    for file in files:
        path = os.path.join(folder, file)
        process_update(path, file)


def check_server():
    while True:
        page = get_url('https://gatherer.wizards.com')
        if 'You Just Exploded the Internet' in page:
            print('Server down!')
            time.sleep(60)
            continue
        else:
            break


def download():
    check_server()
    folder = r'E:\MTG\Oracle'
    files = os.listdir(folder)
    for file in files:
        path = os.path.join(folder, file)
        global threads
        while True:
            if threads < MAX_THREADS:
                if TEST:
                    process_oracle(path, file)
                    exit(1)

                chinese_file = os.path.join('Chinese', file)
                if SKIP_EXIST and os.path.exists(chinese_file):
                    print('Skip!', chinese_file)
                    break

                threads += 1
                print(path, '[' + str(threads) + ']')
                threading.Thread(target=process_oracle, args=(path, file, chinese_file)).start()
                time.sleep(5)
                break
            else:
                time.sleep(10)

    while threads > 0:
        time.sleep(10)


def main():
    download()
    update()


if __name__ == '__main__':
    main()
