import sqlite3
import requests
from time import sleep
from bs4 import BeautifulSoup
from contextlib import closing
from sql_code import create_events, create_coeffs, insert_events
from datetime import datetime as dt


def inserting_coeffs(values):
    with closing(sqlite3.connect("database.db")) as con:
        with closing(con.cursor()) as c:
            columns = ['game_id',
                       'time',
                       'cntry_nm',
                       'league_id',
                       'league_nm',
                       'sport_nm',
                       'opponent_a',
                       'opponent_b',
                       'event_id',
                       'coeff']
            sql = f'INSERT INTO game_coeffs ({", ".join(columns)}) VALUES ({", ".join("?"*len(columns))})'
            c.executemany(sql, values)
            con.commit()


def get_game_data(game_id):
    """
    Метод отправляет запрос, используя id игры, и получает в ответ
    :param game_id: id игры
    :return: возвращает json c данными по конкретной игре
    """
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


def get_games(champ_id):
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
        'champs': champ_id,
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
    Создаёт таблицы events, coeffs
    Добавляет данные в events. Для изменения
    нужно поправить sql-код
    :return:
    """
    with closing(sqlite3.connect("database.db")) as con:
        with closing(con.cursor()) as c:
            sql = create_events()
            c.execute(sql)
            sql = create_coeffs()
            c.execute(sql)
            c.execute('SELECT event_id FROM events LIMIT 1')
            if c.fetchone() is None:
                sql = insert_events()
                c.execute(sql)
                con.commit()


def main():
    create_tables()
    # Футбол
    while True:
        start_time = dt.now()
        champs = get_champs()
        for champ in champs:  # Перебираем список
            start_champ_time = dt.now()
            # 1-й уровень
            print("=" * 100)
            champ_info = get_champ_info(champ)
            print("{} загружается".format(
                champ_info['champ_name']
            ))
            games = get_games(champ_info['id'])
            print(champ_info['id'])
            print("Загружаю {} игр".format(len(games)))
            for game in games:
                game_id = game['I']
                print(game_id)
                game_data = get_game_data(game_id)
                # Резализация логики парсинга кэфов
                coeffs = game_data['GE']
                # Получили все кэфы
                # Смотрим событие 1х2
                winner = coeffs[0]['E']
                event_ids = [1, 2, 3]
                values = list()
                for x in range(3):
                    value = (game_id,
                             dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                             game_data['CN'],
                             game_data['LI'],
                             game_data['L'],
                             game_data['SN'],
                             game_data['O1'],
                             game_data['O2'],
                             event_ids[x],
                             winner[x][0]['C']
                             )
                    values.append(value)
                    print(value)
                values = (*values, )
                inserting_coeffs(values)
                # Смотрим Двойной шанс
                double_chanse = coeffs[1]['E']
                event_ids = [4, 5, 6]
                values = list()
                for x in range(3):
                    value = (game_id,
                             dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                             game_data['CN'],
                             game_data['LI'],
                             game_data['L'],
                             game_data['SN'],
                             game_data['O1'],
                             game_data['O2'],
                             event_ids[x],
                             double_chanse[x][0]['C']
                             )
                    values.append(value)
                    print(value)
                values = (*values, )
                inserting_coeffs(values)
                # total = coeffs[3]['E']
                # fora = coeffs[5]['E']
            end_champ_time = dt.now()
            print("Чемпионат {} загружен за {} секунд".format(
                champ_info['champ_name'],
                (end_champ_time - start_champ_time).total_seconds()
            ))
        break
        end_time = dt.now()
        total_seconds = (end_time - start_time).total_seconds()
        if total_seconds > 60:
            continue
        else:
            sleep(60-total_seconds)


if __name__ == '__main__':
    main()
