import time
import sqlite3
import requests
from contextlib import closing
from sql_code import create_tennis_coeffs
from datetime import datetime as dt


def inserting_coeffs(values):
    with closing(sqlite3.connect("tennis.db")) as con:
        with closing(con.cursor()) as c:
            columns = ['time',
                       'cntry_nm',
                       'league_nm',
                       'tour',
                       'opponent_a',
                       'opponent_b',
                       'event_nm',
                       'event_vl',
                       'coeff']
            sql = f'INSERT INTO coeffs ({", ".join(columns)}) VALUES ({", ".join("?" * len(columns))})'
            c.executemany(sql, values)
            con.commit()


def get_coeffs(game):
    """
    Из данных по игре метод выделяет коэффициенты на группу событий Исход.
    Возвращает список уже готовых к заливке строк.
    :param game: Данные варанта исходов
    :return: Список строк для заливки
    """
    values = list()
    events = game['GE']
    for event in events:
        if event['G'] == 1:  # Достаем победы
            coeffs = event['E']
            for coeff in coeffs:
                if coeff[0]['T'] == 1:
                    value = (game['CI'],
                             dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                             game['CN'],
                             game['LI'],
                             game['L'],
                             game['SN'],
                             game['MIS'][0]['V'],
                             game['O1'],
                             game['O2'],
                             '1x2',
                             '1',
                             coeff[0]['C']
                             )
                    values.append(value)
                elif coeff[0]['T'] == 3:
                    value = (game['CI'],
                             dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                             game['CN'],
                             game['LI'],
                             game['L'],
                             game['SN'],
                             game['MIS'][0]['V'],
                             game['O1'],
                             game['O2'],
                             '1x2',
                             '2',
                             coeff[0]['C']
                             )
                    values.append(value)
        elif event['G'] == 4:  # Достаем Тоталы
            mores = event['E'][0]
            lesses = event['E'][1]
            for more in mores:
                value = (game['CI'],
                         dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                         game['CN'],
                         game['LI'],
                         game['L'],
                         game['SN'],
                         game['MIS'][0]['V'],
                         game['O1'],
                         game['O2'],
                         f'Тотал {more["P"]}',
                         'Б',
                         more['C']
                         )
                values.append(value)
            for less in lesses:
                value = (game['CI'],
                         dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                         game['CN'],
                         game['LI'],
                         game['L'],
                         game['SN'],
                         game['MIS'][0]['V'],
                         game['O1'],
                         game['O2'],
                         f'Тотал {less["P"]}',
                         'М',
                         less['C']
                         )
                values.append(value)
        elif event['G'] == 3:  # Достаем Форы
            firsts = event['E'][0]
            seconds = event['E'][1]
            for first in firsts:
                if 'P' not in first:
                    first['P'] = 0
                value = (game['CI'],
                         dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                         game['CN'],
                         game['LI'],
                         game['L'],
                         game['SN'],
                         game['MIS'][0]['V'],
                         game['O1'],
                         game['O2'],
                         f'Фора {first["P"]}',
                         '1',
                         first['C']
                         )
                values.append(value)
            for second in seconds:
                if 'P' not in second:
                    second['P'] = 0
                value = (game['CI'],
                         dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                         game['CN'],
                         game['LI'],
                         game['L'],
                         game['SN'],
                         game['MIS'][0]['V'],
                         game['O1'],
                         game['O2'],
                         f'Фора {second["P"]}',
                         '2',
                         second['C']
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
        'countevents': '250',
        'partner': '51',
        'grMode': '2',
        'marketType': '1',
        'isNewBuilder': 'true',
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
        'sports': '4',
        'champs': champ_id,
        'count': '50',
        'tf': '2200000',
        'tz': '3',
        'antisports': '188',
        'mode': '4',
        'country': '1',
        'partner': '51',
        'getEmpty': 'true',
    }

    return requests.get(url, params=params).json()['Value']


def create_tables():
    """
    Создаёт таблицы events, coeffs
    Добавляет данные в events. Для изменения
    нужно поправить sql-code.py
    :return: None
    """
    with closing(sqlite3.connect("tennis.db")) as con:
        with closing(con.cursor()) as c:
            sql = create_tennis_coeffs()
            c.execute(sql)


def main():
    create_tables()
    print('старт обхода')
    while True:
        start_time = dt.now()
        with open('tennis_champs.txt') as f:
            # Начинаем обход турниров
            for champ_link in f:
                champ_id = champ_link.split('/')[-1].split('-')[0]
                # Пробуем достать турнир
                try:
                    champ_games = get_games(champ_id)
                except Exception as e:
                    print('НЕ ПОЛУЧИЛОСЬ ДОСТАТЬ ТУРНИР')
                    print(e)
                    continue
                print(champ_id)
                # Обход игра внутри турнира
                for game in champ_games:
                    game_id = game['I']
                    # Пробуем достать игру
                    try:
                        game_data = get_game_info(game_id)
                    except Exception as e:
                        print('НЕ ПОЛУЧИЛОСЬ ДОСТАТЬ ИГРУ')
                        print(e)
                        continue

                    try:
                        insert_rows = get_coeffs(game_data)
                    except Exception as e:
                        print('НЕ ПОЛУЧИЛОСЬ ВСТАВИТЬ КОЭФФИЦИЕНТЫ')
                        print(e)

                    # Пробуем вставить полученные данные в базу
                    try:
                        inserting_coeffs(set(insert_rows))
                    except Exception as e:
                        print('НЕ ПОЛУЧИЛОСЬ ВСТАВИТЬ КОЭФФИЦИЕНТЫ В БАЗУ')
                        print(e)
                        print(game_data)

        # Подсчитываем время обхода чемпионатов
        end_time = dt.now()
        total_seconds = (end_time - start_time).total_seconds()
        print(total_seconds, 'секунд потрачено на чемпионат')
        if total_seconds < 360:
            time.sleep(round(360 - total_seconds))


if __name__ == '__main__':
    main()
