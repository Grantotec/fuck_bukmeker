import time
import sqlite3
import requests
from contextlib import closing
from sql_code import create_football_coeffs
from datetime import datetime as dt


def inserting_coeffs(values):
    with closing(sqlite3.connect("football.db")) as con:
        with closing(con.cursor()) as c:
            columns = ['time',
                       'cntry_nm',
                       'league_nm',
                       'tour',
                       'opponent_a',
                       'opponent_b',
                       'event_nm',
                       'event_vl',
                       'coeff'
                       ]
            sql = f'INSERT INTO coeffs ({", ".join(columns)}) VALUES ({", ".join("?" * len(columns))})'
            c.executemany(sql, values)
            con.commit()


def get_coeffs(game):
    """
    Из данных по игре метод выделяет коэффициенты на группу событий Тотал.
    Возвращает список уже готовых к заливке строк.
    :param game: Данные игры
    :return: Список строк для заливки
    """
    values = list()
    record_time = dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    cntry_nm = game['CN']
    league_nm = game['L']
    tour = game['MIS'][0]['V']
    opponent_a = game['O1']
    opponent_b = game['O2']
    coeffs = game['GE']

    for coeff in coeffs:
        if coeff['G'] == 1:
            # Вытаскиваем исход
            value = (record_time,
                     cntry_nm,
                     league_nm,
                     tour,
                     opponent_a,
                     opponent_b,
                     '1x2',
                     '1',
                     coeff['E'][0][0]['C']
                     )
            values.append(value)

            value = (record_time,
                     cntry_nm,
                     league_nm,
                     tour,
                     opponent_a,
                     opponent_b,
                     '1x2',
                     'x',
                     coeff['E'][1][0]['C']
                     )
            values.append(value)

            value = (record_time,
                     cntry_nm,
                     league_nm,
                     tour,
                     opponent_a,
                     opponent_b,
                     '1x2',
                     '2',
                     coeff['E'][2][0]['C']
                     )
            values.append(value)

        if coeff['G'] == 3:
            # Вытаскиваем Фора
            first = coeff['E'][0]
            second = coeff['E'][1]

            for fora in first:
                fora_sign = fora['P'] if 'P' in fora else 0

                value = (record_time,
                         cntry_nm,
                         league_nm,
                         tour,
                         opponent_a,
                         opponent_b,
                         'Ф ' + str(fora_sign),
                         '1',
                         fora['C']
                         )
                values.append(value)

            for fora in second:
                fora_sign = fora['P'] if 'P' in fora else 0

                value = (record_time,
                         cntry_nm,
                         league_nm,
                         tour,
                         opponent_a,
                         opponent_b,
                         'Ф ' + str(fora_sign),
                         '2',
                         fora['C']
                         )
                values.append(value)

        if coeff['G'] == 4:
            # Вытаскиваем Тотал
            more = coeff['E'][0]
            less = coeff['E'][1]

            for total in more:
                total_sign = total['P'] if 'P' in total else 0

                value = (record_time,
                         cntry_nm,
                         league_nm,
                         tour,
                         opponent_a,
                         opponent_b,
                         'T ' + str(total_sign),
                         'Б',
                         total['C']
                         )
                values.append(value)

            for total in less:
                total_sign = total['P'] if 'P' in total else 0

                value = (record_time,
                         cntry_nm,
                         league_nm,
                         tour,
                         opponent_a,
                         opponent_b,
                         'T ' + str(total_sign),
                         'М',
                         total['C']
                         )
                values.append(value)

    return values


def get_game_info(game_id):
    """
        Метод отправляет запрос, используя id игры, и получает в ответ
        :param game_id: id игры
        :return: возвращает json c данными по конкретной игре

        https://1xstavka.ru/LineFeed/GetGameZip?id=156129205&lng=ru&cfview=0&isSubGames=true&GroupEvents=true&
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
        'tz': '3',
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
    with closing(sqlite3.connect("football.db")) as con:
        with closing(con.cursor()) as c:
            sql = create_football_coeffs()
            c.execute(sql)


def main():
    create_tables()
    print('старт обхода')
    while True:
        start_time = dt.now()
        with open('champs.txt') as f:
            # Начинаем обход турниров
            for champ_link in f:
                print('=' * 200)
                print('старт чемпионата')
                champ_id = champ_link.split('/')[-1].split('-')[0]
                # Пробуем достать турнир
                try:
                    champ_games = get_games(champ_id)
                except Exception as e:
                    print('НЕ ПОЛУЧИЛОСЬ ДОСТАТЬ ТУРНИР')
                    print(e)
                    continue
                # Обход игра внутри турнира
                for game in champ_games:
                    if 'O1' in game and 'O2' in game:
                        if 'Хозяева' in game['O1'] or 'Гости' in game['O2']:
                            continue
                    else:
                        continue

                    game_id = game['CI']
                    print(game['LI'], game['L'])
                    print(game['O1'], ' - ', game['O2'], '   ', game_id)  # Печатаем названия команд
                    # Пробуем достать игру
                    try:
                        game_data = get_game_info(game_id)
                    except Exception as e:
                        print('НЕ ПОЛУЧИЛОСЬ ДОСТАТЬ ИГРУ')
                        print(e)
                        print(game_data)
                        continue

                    try:
                        insert_rows = get_coeffs(game_data)
                    except Exception as e:
                        print('НЕ ПОЛУЧИЛОСЬ ДОСТАТЬ КОЭФФИЦИЕНТЫ')
                        print(e)
                        print(game_data)
                        continue

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


if __name__ == "__main__":
    main()
