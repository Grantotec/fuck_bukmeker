import sqlite3
import requests
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


def get_coeffs(indxs, game):
    values = list()
    for x in indxs:
        value = (game['CI'],
                 dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                 game['CN'],
                 game['LI'],
                 game['L'],
                 game['SN'],
                 game['O1'],
                 game['O2'],
                 x + 1,
                 game['E'][x]['C']
                 )
        values.append(value)
    return values


def get_game_info(game_id, champ_id):
    """
        Метод отправляет запрос, используя id игры, и получает в ответ
        :param game_id: id игры
        :param champ_id: id Чемпионата
        :return: возвращает json c данными по конкретной игре

        https://1xstavka.ru/LineFeed/Get1x2?sports=1&champs=119237&count=50&tf=2200000&tz=3&antisports=188&mode=4&subGames=1559171078country=1&partner=51&getEmpty=true
    """
    url = 'https://1xstavka.ru/LineFeed/Get1x2'
    params = {
        'sports': '1',
        'champs': champ_id,
        'count': '50',
        'tf': '2200000',
        'tz': '3',
        'antisports': '188',
        'mode': '4',
        'subGames': game_id,
        'GroupEvents': 'true',
        'country': '1',
        'partner': '51',
        'getEmpty': 'true'
    }
    return requests.get(url, params=params).json()['Value']


def get_games(champ_id):
    """
    Метод отправляет запрос, используя id чемпионата, и полдучает в ответ данные
    чемпионата.
    :return: возвращает json c данными. Данные содержат id всех игр внутри
    конкретного чемпионата.

    URL
    https://1xstavka.ru/LineFeed/Get1x2_VZip?sports=1&champs=33&count=10&tf=2200000&tz=3&antisports=188&mode=4&country=1&partner=51&getEmpty=true
    """
    url = 'https://1xstavka.ru/LineFeed/Get1x2_VZip'
    params = {
        'sports': '1',
        'champs': champ_id,
        'count': '50',
        'tf': '2200000',
        'antisports': '188',
        'mode': '4',
        'country': '1',
        'partner': '51',
        'getEmpty': 'true'
    }
    return requests.get(url, params=params).json()['Value']


def create_tables():
    """
    Создаёт таблицы events, coeffs
    Добавляет данные в events. Для изменения
    нужно поправить sql-code.py
    :return: None
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
    with open('champs.txt') as f:
        start_time = dt.now()
        for champ_link in f:
            print('старт обхода')
            champ_id = champ_link.split('/')[-1].split('-')[0]
            champ_games = get_games(champ_id)
            for game in champ_games:
                print(game['LI'], game['L'])
                print(game['O1'], ' - ', game['O2'])  # Печатаем названия команд
                events_result = list()  # Все новые строки в базу
                events_result += get_coeffs([0, 1, 2], game)  # Смотрим событие 1х2
                events_result += get_coeffs([3, 4, 5], game)  # Смотрим Двойной шанс
                events_result = (*events_result,)
                # inserting_coeffs(events_result)
                for value in events_result:
                    print(value)

        end_time = dt.now()
        total_seconds = (end_time - start_time).total_seconds()
        print(total_seconds, 'секунд потрачено на чемпионат')


if __name__ == "__main__":
    main()