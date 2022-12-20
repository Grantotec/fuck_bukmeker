import requests
from bs4 import BeautifulSoup


def get_game_info(game_id):

    url = 'https://1xstavka.ru/LineFeed/GetGameZip'
    params = {
        "game_id": game_id,
        'id': '151027435',
        'lng': 'ru',
        'cfview': '0',
        'isSubGames': 'false',
        'GroupEvents': 'true',
        'allEventsGroupSubGames': 'true',
        'countevents': '250',
        'partner': '51',
        'grMode': '2',
        'marketType': '1',
        'isNewBuilder': 'true'
    }
    response = requests.get(url, params=params).json()['Value']
    game_info = response['GE']
    return game_info


def get_games(champ_info):
    url = 'https://1xstavka.ru/LineFeed/Get1x2_VZip'
    params = {
        'sports': '1',
        'champs': champ_info['id'],
        'count': '300',
        'tf': '2200000',
        'tz': '3',
        'antisports': '188',
        'mode': '4',
        'country': '1',
        'partner': '51',
        'getEmpty': 'true'
    }

    return requests.get(url, params=params).json()['Value']


def get_champ_info(champ):
    champ_info = dict()
    champ_info['id'] = champ.get('href').split('/')[-1].split('-')[0]
    champ_info['games_count'] = str(champ.find('span', 'link-title__count').contents[0])
    champ_info['champ_name'] = str(champ.find('span', 'link-title__label').contents[0])

    return champ_info


def get_champs():
    page = requests.get('https://1xstavka.ru/line/football')
    soup = BeautifulSoup(page.text, 'html.parser')
    champs = soup.find_all('a', ['link link--labled'])

    return champs


def main():
    # Футбол
    for champ in get_champs():  # Перебираем список
        # 1-й уровень
        print("=" * 100)
        champ_info = get_champ_info(champ)
        for game in get_games(champ_info):
            game_id = game['CI']
            game_info = get_game_info(game_id)
            print(game_info)
        break
    # db = sqlite3.connect('database.db')



if __name__ == '__main__':
    main()
