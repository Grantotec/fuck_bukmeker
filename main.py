import sqlite3
import requests
from bs4 import BeautifulSoup
from contextlib import closing
from sql_code import create_events, create_coeffs, insert_events
# from datetime import datetime as dt


def upload_game_data(game_info):
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute(
            '''
            INSERT INTO coeffs (
                game_id,
                game_name,
                game_description,
                game_url,
                game_image'''
        )


def get_game_data(game_id):
    """
    Метод отправляет запрос, используя id игры, и получает в ответ
    :param game_id: id игры
    :return: возвращает json c данными по конкретной игре
    """
    game_info = dict()
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
    return requests.get(url, params=params).json()['Value']


def get_games(champ_info):
    """
    Метод отправляет запрос, используя id чемпионата,
    и полдучает в ответ данные чемпионата.

    :param champ_info: словарь с данными по чемпионату
    :return: возвращает json c данными. Данные содержат id
    всех игр внутри конкретного чемпионата.
    """
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
    """
    Метод собирает данные по чемпионату. id нам понадобится
    для дальнейшего получения данных по играм.

    :param champ: Чемпионат
    :return: Возвращает словарь с данными по чемпионату
    """
    champ_info = dict()
    champ_info['id'] = champ.get('href').split('/')[-1].split('-')[0]
    champ_info['games_count'] = str(champ.find('span', 'link-title__count').contents[0])
    champ_info['champ_name'] = str(champ.find('span', 'link-title__label').contents[0])

    return champ_info


def get_champs():
    """
    При итерировании по этому методу перебираются
    чемпионаты внутри футбола.

    :return: Возвращает список чемпионатов
    """
    page = requests.get('https://1xstavka.ru/line/football')
    soup = BeautifulSoup(page.text, 'html.parser')
    champs = soup.find_all('a', ['link link--labled'])

    return champs


def create_tables():
    """
    TODO страшно ли? если существуют данные, программа
    TODO повторно будет пытать создать существующие таблицы

    Создаёт таблицы events, coeffs
    :return:
    """
    with closing(sqlite3.connect("database.db")) as connection:
        with closing(connection.cursor()) as cursor:
            sql = create_events()
            cursor.execute(sql)
            sql = create_coeffs()
            cursor.execute(sql)
            cursor.execute('SELECT event_id FROM events LIMIT 1')
            if cursor.fetchone() is None:
                sql = insert_events()
                cursor.execute(sql)
                connection.commit()


def main():
    create_tables()
    # Футбол
    for champ in get_champs():  # Перебираем список
        # 1-й уровень
        print("=" * 100)
        champ_info = get_champ_info(champ)
        for game in get_games(champ_info):
            game_id = game['CI']
            game_data = get_game_data(game_id)
            print(game_data)
            # upload_game_data(game_data)
        break


if __name__ == '__main__':
    main()
