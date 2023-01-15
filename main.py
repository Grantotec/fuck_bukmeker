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


def get_fora(game):
    """
    TODO дописать функцию
    Из данных по игре метод выделяет коэффициенты на группу событий Фора.
    Возвращает список уже готовых к заливке строк.
    :param game: Данные игры
    :return: Список строк для заливки
    """
    pass


def get_total(game):
    """
    TODO дописать функцию
    Из данных по игре метод выделяет коэффициенты на группу событий Тотал.
    Возвращает список уже готовых к заливке строк.
    :param game: Данные игры
    :return: Список строк для заливки
    """
    pass


def get_dvoynoy_shans(game):
    """
    Из данных по игре метод выделяет коэффициенты на группу событий Двойной шанс.
    Возвращает список уже готовых к заливке строк.
    :param game: Данные игры
    :return: Список строк для заливки
    """
    values = list()
    coeffs = game['GE'][1]['E']
    for x in range(3):
        value = (game['CI'],
                 dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                 game['CN'],
                 game['LI'],
                 game['L'],
                 game['SN'],
                 game['O1'],
                 game['O2'],
                 x + 4,
                 coeffs[x][0]['C']
                 )
        values.append(value)
    return values


def get_isxod(game):
    """
    Из данных по игре метод выделяет коэффициенты на группу событий Исход.
    Возвращает список уже готовых к заливке строк.
    :param game: Данные игры
    :return: Список строк для заливки
    """
    values = list()
    coeffs = game['GE'][0]['E']
    for x in range(3):
        value = (game['CI'],
                 dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                 game['CN'],
                 game['LI'],
                 game['L'],
                 game['SN'],
                 game['O1'],
                 game['O2'],
                 x + 1,
                 coeffs[x][0]['C']
                 )
        values.append(value)
    return values


def get_game_info(game_id):
    """
        Метод отправляет запрос, используя id игры, и получает в ответ
        :param game_id: id игры
        :return: возвращает json c данными по конкретной игре

        https://1xstavka.ru/LineFeed/GetGameZip?id=156129205&lng=ru&cfview=0&isSubGames=tru&GroupEvents=true&
        allEventsGroupSubGames=true&countevents=250&partner=51&grMode=2&marketType=1&isNewBuilder=true
    """
    url = 'https://1xstavka.ru/LineFeed/GetGameZip'
    params = {
        'id': game_id,
        'lng': 'ru',
        'cfview': '0',
        'isSubGames': 'true',
        'GroupEvents': 'true',
        'allEventsGroupSubGames': 'true',
        'countevents': '1000',
        'partner': '51',
        'grMode': '2',
        'marketType': '1',
        'isNewBuilder': 'true'
    }
    return requests.get(url, params=params).json()['Value']


def get_games(champ_id):
    """
    Метод отправляет запрос, используя id чемпионата, и получает в ответ данные
    чемпионата.
    :return: возвращает json c данными. Данные содержат id всех игр внутри
    конкретного чемпионата.

    URL
    https://1xstavka.ru/LineFeed/Get1x2_VZip?sports=1&champs=33&count=10&tf=2200000&tz=3&antisports=188&mode=4&
    country=1&partner=51&getEmpty=true
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
    print('старт обхода')
    with open('champs.txt') as f:
        start_time = dt.now()
        for champ_link in f:
            print('=' * 200)
            print('старт чемпионата')
            champ_id = champ_link.split('/')[-1].split('-')[0]
            champ_games = get_games(champ_id)
            for game in champ_games:
                if 'Хозяева' in game['O1'] or 'Гости' in game['O2']:
                    continue
                rows = list()
                game_id = game['CI']
                print(game['LI'], game['L'])
                print(game['O1'], ' - ', game['O2'], '   ', game_id)  # Печатаем названия команд
                game_info = get_game_info(game_id)
                rows += get_isxod(game_info)
                rows += get_dvoynoy_shans(game_info)
                # rows += get_total(game_info)
                # rows += get_fora(game_info)
                # inserting_coeffs(set(rows))
                for row in rows:
                    print(row)

        # Подсчитываем время обхода чемпионатов
        end_time = dt.now()
        total_seconds = (end_time - start_time).total_seconds()
        print(total_seconds, 'секунд потрачено на чемпионат')


if __name__ == "__main__":
    main()
