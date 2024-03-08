import os
import re
import time
import zipfile

import requests

deck_folder = 'mtggoldfish'

forge_cards = []
skip_url = []
meta_folder = ''
deck_index = 1


def get_post(meta, page):
    while True:
        try:
            data = 'utf8=%E2%9C%93&period=365&mformat=' + meta + '&page=' + str(page) + '&type=paper&full=1'
            headers = {
                'Cookie': '_dlt=1; _ga=GA1.2.1061852238.1664654711; _pbjs_userid_consent_data=3524755945110770; _lr_env_src_ats=false; __gads=ID=7dec9fd7bdafe086-228b929fd4d6001d:T=1664654717:S=ALNI_Ma1xr4HLKQON-pXYGX3c_l_79zH8w; __gpi=UID=00000a16df0544e1:T=1664654717:RT=1665796210:S=ALNI_MYzPWd7QE0ffo2NuZODY73REDbj8w; cto_bundle=J1d64V9oUHVHcHpHZTV0M0dOY21GTmJKQzBOODNsazFpSSUyQnhoOHVZUHhRMFJTb1hFRVklMkJ2R09nTFY5YjJZcnRFN2JXTjlSTGo0UllhdHhMVWQ5Qkw3OUYxSWlNdDVZV3FYREZxbVFyYXhIZlUlMkJpNFRrY2daMjRzYU9QVktzbGc0YmhtMjdTWThGdnd1RER4dDJWQ1c4cDNGJTJGUSUzRCUzRA; cto_bidid=_T0yzV8lMkI4VnBkeTVBSHNFQ1JmaVFFUXp6NVV5T1JzUlllVHR1V3UwRXI2cSUyQk1ieFRtckVVaGl5RDE1WU84YkE1aXlGdktBanNaTFVTYTNyYXhRWVhWSzAwcXZFWndBeUNZM2NRJTJGd0l0JTJCNjFRJTJGenpXTEdaRTlIR3ZxTDliVW1DWll5Vm8; _mtg_session=elIrM3ZUd2hSQjk2VXlwbmtuNDRDL0JOelFTSmN6dU1qbWRIM2VWeUJhOHpscFhNVy9IdEs5WUh5K0RHVHVubldsWDdYUmZ1QVdDS2g4c3A2TXY4dGMrZ0c4Slo1cVFmK2dMbW9PaThsN3dDNDNiVmszcE9ZU09wVkhubGRMY3lkdGtPbkg5Rnd4ZzR3dkxEbUc2UkJpYVduem5Da1BQNGZnMTFKZW8wTHFuUVRZMGk3KzMwTm53bnlkRGo5emkrNTdiU25pdHV5S0hnTDFoeWNIcFEzdUtZNlVkTThQRFdWUHVZbC9yN0lScz0tLVBkZ3dhS3IyWU43TjdtUm9CemJtdlE9PQ%3D%3D--4f60f6929b65eee708789630c075c4265ddfb6bd; _gid=GA1.2.1929402373.1665796205; _lr_geo_location=CN; _gat=1; _gali=metagame-re-sort-select',
                'X-CSRF-Token': 'JNtsfb87RGRaca/qgibSP65OsjktwwY8EL0vncnTVUPENpzhqE21lazLYh59NqTF2GxjBM+TpA410Zesmwja8Q==',
            }
            content = requests.post('https://www.mtggoldfish.com/metagame/re_sort', data=data, headers=headers,
                                    timeout=60)
            if content.status_code != 200:
                print('Code', content.status_code)
                time.sleep(60)
                continue
            break
        except Exception as e:
            print(e)
    return content.text


def get_url(url):
    while True:
        try:
            content = requests.get(url, timeout=60)
            if len(content.text) < 16:
                print('Throttled!', url)
                time.sleep(60)
                continue
            break
        except Exception as e:
            print(e)
    return content.text


def fix_deck(name, all_cards, url):
    missing_cards = {}

    print('fixing =>', 'https://www.mtggoldfish.com' + url)

    url = url[:url.index('?')]
    print('txt =>', 'https://www.mtggoldfish.com' + url)
    content = get_url('https://www.mtggoldfish.com' + url)

    with open(os.path.join(deck_folder, meta_folder, name + '.txt'), 'w', encoding='utf8') as file:
        file.write(content)

    with open(os.path.join(deck_folder, meta_folder, name + '.txt'), 'r', encoding='utf8') as file:
        for line in file.readlines():
            result = re.search(r'(\d+) (.*?)[\r\n]', line)
            if result:
                card_name = result.group(2).replace('&#39;', "'").replace('&quot;', '"').replace('&amp;', '&')
                if card_name not in all_cards:
                    if '/' in card_name:
                        card_name = card_name.replace('/', ' // ')
                        missing_cards[card_name] = missing_cards.get(card_name, 0) + int(result.group(1))
                    else:
                        if card_name not in forge_cards:
                            print('Card "' + card_name + '" Not Found in fixing!')
                            return None
                        print('Add back "' + card_name + '"')
                        missing_cards[card_name] = missing_cards.get(card_name, 0) + int(result.group(1))

    return missing_cards


def convert_deck(name, path, url):
    global deck_index

    main_cards = {}
    side_cards = {}
    all_cards = []
    main_num = 0
    side_num = 0
    with open(path, 'r', encoding='utf8') as file:
        for line in file.readlines():
            result = re.search(r'Quantity="(\d+)" Sideboard="(.*?)" Name="(.*?)"', line)
            if result:
                card_name = result.group(3).replace('&#39;', "'").replace('&quot;', '"').replace('&amp;', '&')
                all_cards.append(card_name)
                if '/' in card_name:
                    main_num += int(result.group(1))
                    card_name = card_name.replace('/', ' // ')
                    main_cards[card_name] = main_cards.get(card_name, 0) + int(result.group(1))
                else:
                    if card_name not in forge_cards:
                        print('Card "' + card_name + '" Not Found!')
                        return False
                    if ('commander' in meta_folder or 'brawl' in meta_folder) and (card_name == name or
                       ('+' in name and (name.startswith(card_name) or name.endswith(card_name)))):
                        side_num += int(result.group(1))
                        side_cards[card_name] = side_cards.get(card_name, 0) + int(result.group(1))
                    elif result.group(2) == 'false':
                        main_num += int(result.group(1))
                        main_cards[card_name] = main_cards.get(card_name, 0) + int(result.group(1))
                    else:
                        side_num += int(result.group(1))
                        side_cards[card_name] = side_cards.get(card_name, 0) + int(result.group(1))

    if 'commander' in meta_folder or 'brawl' in meta_folder:
        print(main_num + side_num, 'cards in deck,', side_num, 'commander(s)')
        if meta_folder == 'brawl':
            deck_cards = 60
        else:
            deck_cards = 100
        if main_num + side_num != deck_cards:
            if url:
                missing_cards = fix_deck(name, all_cards, url)
                if missing_cards is None:
                    return False
                if missing_cards:
                    for card, num in missing_cards.items():
                        if card == name or ('+' in name and (name.startswith(card) or name.endswith(card))):
                            side_num += num
                            side_cards[card] = side_cards.get(card, 0) + num
                        else:
                            main_num += num
                            main_cards[card] = main_cards.get(card, 0) + num
                print('After fixing =>', main_num + side_num, 'cards in deck,', side_num, 'commander(s)')

        if main_num + side_num != deck_cards or side_num == 0 or side_num > 2:
            print('Invalid deck!')
            return False
    else:
        print(main_num + side_num, 'cards in deck,', side_num, 'sideboard')
        if (main_num != 60 and main_num != 80) or side_num != 15:
            print('Invalid deck!')
            return False

    path = path.replace('.dek', '.dck').replace(os.path.join(deck_folder, meta_folder, ''),
                                                os.path.join(deck_folder, meta_folder, str(deck_index) + '. '))
    with open(path, 'w') as file:
        file.write('[metadata]\n')
        file.write('Name=' + name + '\n')
        if 'commander' in meta_folder or 'brawl' in meta_folder:
            file.write('[Commander]\n')
            for card in sorted(side_cards.keys()):
                file.write(str(side_cards[card]) + ' ' + card + '\n')
        file.write('[Main]\n')
        for card in sorted(main_cards.keys()):
            file.write(str(main_cards[card]) + ' ' + card + '\n')
        if not ('commander' in meta_folder or 'brawl' in meta_folder):
            file.write('[Sideboard]\n')
            for card in sorted(side_cards.keys()):
                file.write(str(side_cards[card]) + ' ' + card + '\n')

    print('Saved', '=>', path)

    deck_index += 1
    return True


def get_deck(name, date, tix, url):
    print('Get deck', name, date, tix.replace(',', ''), 'tix')
    print(name, 'deck =>', 'https://www.mtggoldfish.com' + url)

    url = url.replace('/deck/', '/deck/download/')
    url += '?output=dek&type=online'
    content = get_url('https://www.mtggoldfish.com' + url)

    if 'The deck you are trying to view has been marked as private.' in content:
        print('Private deck!')
        return False

    with open(os.path.join(deck_folder, meta_folder, name + '.dek'), 'w', encoding='utf8') as file:
        file.write(content)

    if convert_deck(name, os.path.join(deck_folder, meta_folder, name + '.dek'), url):
        print('Got deck =>', name, date, tix.replace(',', ''), 'tix')
        print('-' * 20)
        return True

    return False


def get_archetype_page(name, archetype):
    print(name, '=>', 'https://www.mtggoldfish.com/archetype/' + archetype)

    index = 1
    while True:
        if index == 1:
            page_url = 'https://www.mtggoldfish.com/archetype/' + archetype + '/decks'
        else:
            page_url = 'https://www.mtggoldfish.com/archetype/' + archetype + '/decks?page=' + str(index)
        print(name, '=>', page_url)
        content = get_url(page_url)

        matches = re.findall(r'<td>(\d\d\d\d-\d\d-\d\d)</td>.*?<a href="(/deck/\d+)".*?>([\d,]+).tix',
                             content.replace('\r', '').replace('\n', ''))

        for date, url, tix in matches:
            if date.startswith('2022'):
                if int(tix.replace(',', '')) > 200 and url not in skip_url:
                    if get_deck(name, date, tix, url):
                        return True
                    else:
                        skip_url.append(url)

        for date, url, tix in matches:
            if date.startswith('2022'):
                if int(tix.replace(',', '')) > 100 and url not in skip_url:
                    if get_deck(name, date, tix, url):
                        return True
                    else:
                        skip_url.append(url)

        for date, url, tix in matches:
            if date.startswith('202'):
                if int(tix.replace(',', '')) > 200 and url not in skip_url:
                    if get_deck(name, date, tix, url):
                        return True
                    else:
                        skip_url.append(url)

        for date, url, tix in matches:
            if date.startswith('202'):
                if int(tix.replace(',', '')) > 100 and url not in skip_url:
                    if get_deck(name, date, tix, url):
                        return True
                    else:
                        skip_url.append(url)

        for date, url, tix in matches:
            if date.startswith('202'):
                if int(tix.replace(',', '')) > 50 and url not in skip_url:
                    if get_deck(name, date, tix, url):
                        return True
                    else:
                        skip_url.append(url)

        if meta_folder == 'penny_dreadful':
            for date, url, tix in matches:
                if get_deck(name, date, tix, url):
                    return True

        index += 1
        if '/archetype/' + archetype + '/decks?page=' + str(index) not in content:
            break

    return False


def get_archetypes(archetypes):
    global skip_url
    skip_url = []
    for url, name in archetypes:
        name = name.replace('&#39;', "'").replace('&quot;', "'").replace('&amp;', '&') \
            .replace('\uFE0F', ' ').replace('//', '+').replace('/', '-').strip()
        if ('commander' in meta_folder or 'brawl' in meta_folder) and '+' not in name and name not in forge_cards:
            print('Skip >>> ', name)
            print('=' * 20)
            continue
        found = False
        for file in os.listdir(os.path.join(deck_folder, meta_folder)):
            if file.endswith('. ' + name + '.dck'):
                found = True
                break
        if found:
            print('Skip exist', name)
            print('=' * 20)
            continue
        if not get_archetype_page(name, url):
            print('>>> No deck for', name)
            print('=' * 20)


def get_meta(meta):
    print('Get meta', meta)

    archetypes = []
    page = 1
    while True:
        content = get_post(meta, page)
        matches = re.findall(r'<a href="/archetype/([^/]*?)#paper">(.*?)</a>', content.replace('\\', ''))
        print('Page', page, 'Archetypes', len(matches))
        if matches:
            archetypes += matches
        else:
            if page == 1:
                print('Page 1 no archetype?', content)
                time.sleep(60)
                continue
            else:
                break
        page += 1

    get_archetypes(archetypes)


def get_page(url):
    print('Get page', url)

    content = get_url(url)

    matches = re.findall(r'<a href="/archetype/(.*?)#paper">(.*?)</a>', content)

    get_archetypes(matches)


def get_forge_cards():
    with zipfile.ZipFile(r'E:\Forge\2022\res\cardsfolder\cardsfolder.zip', 'r') as zip_file:
        for name in zip_file.namelist():
            if name.lower().endswith('.txt'):
                file = zip_file.open(name)
                card_text = file.read().decode('utf-8')
                result = re.search(r'Name:([^\r\n]+)', card_text)
                if result:
                    forge_cards.append(result.group(1))
                else:
                    print(name + 'No Name error!')
                    exit(0)
                file.close()


def download_meta(meta, start=None, end=None):
    global meta_folder
    global deck_index

    if not end:
        end = start

    deck_index = 1
    meta_folder = meta

    if not os.path.exists(os.path.join(deck_folder, meta_folder)):
        os.makedirs(os.path.join(deck_folder, meta_folder))

    if start:
        for i in range(start, end + 1):
            get_page('https://www.mtggoldfish.com/metagame/' + meta + '/full?page=' + str(i) + '#paper')
    else:
        get_meta(meta)


def main():
    get_forge_cards()

    # download_meta('commander', 1, 17)
    download_meta('commander')


if __name__ == '__main__':
    main()
