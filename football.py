import time
import sqlite3
import requests
from contextlib import closing
from sql_code import create_events, create_coeffs, insert_events
from datetime import datetime as dt


TOTALS_SIGN_MORE = {
    '0': '7',
    '0.5': '8',
    '1': '9',
    '1.5': '10',
    '2': '11',
    '2.5': '12',
    '3': '13',
    '3.5': '14',
    '4': '15',
    '4.5': '16',
    '5': '17',
    '5.5': '18',
    '6': '19',
    '6.5': '20',
    '7': '21',
    '7.5': '22',
    '8': '23',
    '8.5': '24',
    '9': '25',
    '9.5': '26',
    '10': '27'
}

TOTALS_SIGN_LESS = {
    '0': '45',
    '0.5': '46',
    '1': '47',
    '1.5': '48',
    '2': '49',
    '2.5': '50',
    '3': '51',
    '3.5': '52',
    '4': '53',
    '4.5': '54',
    '5': '55',
    '5.5': '56',
    '6': '57',
    '6.5': '58',
    '7': '59',
    '7.5': '60',
    '8': '61',
    '8.5': '62',
    '9': '63',
    '9.5': '64',
    '10': '65'
}

FORA_SIGN_FIRST = {
    '5': '86',
    '4.5': '87',
    '4': '88',
    '3.5': '89',
    '3': '90',
    '2.5': '91',
    '2': '92',
    '1.5': '93',
    '1': '94',
    '0.5': '95',
    '0': '96',
    '-0.5': '97',
    '-1': '98',
    '-1.5': '99',
    '-2': '100',
    '-2.5': '101',
    '-3': '102',
    '-3.5': '103',
    '-4': '104',
    '-4.5': '105',
    '-5': '106'
}

FORA_SIGN_SECOND = {
    '5': '107',
    '4.5': '108',
    '4': '109',
    '3.5': '110',
    '3': '111',
    '2.5': '112',
    '2': '113',
    '1.5': '114',
    '1': '115',
    '0.5': '116',
    '0': '117',
    '-0.5': '118',
    '-1': '119',
    '-1.5': '120',
    '-2': '121',
    '-2.5': '122',
    '-3': '123',
    '-3.5': '124',
    '-4': '125',
    '-4.5': '126',
    '-5': '127'
}


def inserting_coeffs(values):
    with closing(sqlite3.connect("database.db")) as con:
        with closing(con.cursor()) as c:
            columns = ['game_id',
                       'time',
                       'cntry_nm',
                       'league_id',
                       'league_nm',
                       'sport_nm',
                       'tour',
                       'opponent_a',
                       'opponent_b',
                       'event_id',
                       'coeff']
            sql = f'INSERT INTO coeffs ({", ".join(columns)}) VALUES ({", ".join("?" * len(columns))})'
            c.executemany(sql, values)
            con.commit()


def get_total_ugl(game):
    """
    Из данных по игре метод выделяет коэффициенты на группу событий Тотал Угловых.
    Возвращает список уже готовых к заливке строк.
    :param game:
    :return:
    """

    pass


def get_fora(game):
    """
    Из данных по игре метод выделяет коэффициенты на группу событий Фора.
    Возвращает список уже готовых к заливке строк.
    :param game: Данные игры
    :return: Список строк для заливки
    """
    global FORA_SIGN_FIRST, FORA_SIGN_SECOND

    values = list()
    coeffs = game['GE'][5]['E']
    first = coeffs[0]
    second = coeffs[1]

    for fora in first:
        if 'P' not in fora:
            fora_sign = '0'
        else:
            fora_sign = str(fora['P'])

        coeff_sign = int(FORA_SIGN_FIRST[fora_sign])

        value = (game['CI'],
                 dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                 game['CN'],
                 game['LI'],
                 game['L'],
                 game['SN'],
                 game['MIS'][0]['V'].split(' ')[1],
                 game['O1'],
                 game['O2'],
                 coeff_sign,
                 fora['C']
                 )

        values.append(value)

    for fora in second:
        if 'P' not in fora:
            fora_sign = '0'
        else:
            fora_sign = str(fora['P'])

        coeff_sign = int(FORA_SIGN_SECOND[fora_sign])

        value = (game['CI'],
                 dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                 game['CN'],
                 game['LI'],
                 game['L'],
                 game['SN'],
                 game['MIS'][0]['V'].split(' ')[1],
                 game['O1'],
                 game['O2'],
                 coeff_sign,
                 fora['C']
                 )

        values.append(value)

    return values


def get_total(game):
    """
    Из данных по игре метод выделяет коэффициенты на группу событий Тотал.
    Возвращает список уже готовых к заливке строк.
    :param game: Данные игры
    :return: Список строк для заливки
    """
    global TOTALS_SIGN_MORE, TOTALS_SIGN_LESS

    values = list()
    coeffs = game['GE'][3]['E']
    more = coeffs[0]
    less = coeffs[1]

    for total in more:
        if 'P' not in total:
            total_sign = '0'
        else:
            total_sign = str(total['P'])

        coeff_sign = int(TOTALS_SIGN_MORE[total_sign])

        value = (game['CI'],
                 dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                 game['CN'],
                 game['LI'],
                 game['L'],
                 game['SN'],
                 game['MIS'][0]['V'].split(' ')[1],
                 game['O1'],
                 game['O2'],
                 coeff_sign,
                 total['C']
                 )

        values.append(value)

    for total in less:
        if 'P' not in total:
            total_sign = '0'
        else:
            total_sign = str(total['P'])

        coeff_sign = int(TOTALS_SIGN_LESS[total_sign])

        value = (game['CI'],
                 dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                 game['CN'],
                 game['LI'],
                 game['L'],
                 game['SN'],
                 game['MIS'][0]['V'],
                 game['O1'],
                 game['O2'],
                 coeff_sign,
                 total['C']
                 )

        values.append(value)

    return values


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
                 game['MIS'][0]['V'].split(' ')[1],
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
                 game['MIS'][0]['V'].split(' ')[1],
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
        'getEmpty': 'getEmpty'
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
                    if 'Хозяева' in game['O1'] or 'Гости' in game['O2']:
                        continue
                    rows = list()
                    game_id = game['CI']
                    print(game['LI'], game['L'])
                    print(game['O1'], ' - ', game['O2'], '   ', game_id)  # Печатаем названия команд
                    # Пробуем достать игру
                    try:
                        game_info = get_game_info(game_id)
                    except Exception as e:
                        print('НЕ ПОЛУЧИЛОСЬ ДОСТАТЬ ИГРУ')
                        print(e)
                        print(game_info)
                        continue

                    # Пробуем достать Исход
                    try:
                        rows += get_isxod(game_info)
                    except Exception as e:
                        print('НЕ ПОЛУЧИЛОСЬ ВЫТАЩИТЬ ИСХОД')
                        print(e)
                        print(game_info)

                    # Пробуем достать Двойной шанс
                    try:
                        rows += get_dvoynoy_shans(game_info)
                    except Exception as e:
                        print('НЕ ПОЛУЧИЛОСЬ ВЫТАЩИТЬ ДВОЙНОЙ ШАНС')
                        print(e)
                        print(game_info)

                    # Пробуем достать Тотал
                    try:
                        rows += get_total(game_info)
                    except Exception as e:
                        print('НЕ ПОЛУЧИЛОСЬ ВЫТАЩИТЬ ТОТАЛ')
                        print(e)
                        print(game_info)

                    try:
                        rows += get_fora(game_info)
                    except Exception as e:
                        print('НЕ ПОЛУЧИЛОСЬ ВЫТАЩИТЬ ФОРУ')
                        print(e)
                        print(game_info)

                    try:
                        rows += get_total_ugl(game_info)
                    except Exception as e:
                        print('НЕ ПОЛУЧИЛОСЬ ВЫТАЩИТЬ ТОТАЛ УГЛОВЫХ')
                        print(e)
                        print(game_info)

                    # Пробуем вставить полученные данные в базу
                    try:
                        inserting_coeffs(set(rows))
                    except Exception as e:
                        print('НЕ ПОЛУЧИЛОСЬ ВСТАВИТЬ КОЭФФИЦИЕНТЫ В БАЗУ')
                        print(e)
                        print(game_info)

        # Подсчитываем время обхода чемпионатов
        end_time = dt.now()
        total_seconds = (end_time - start_time).total_seconds()
        print(total_seconds, 'секунд потрачено на чемпионат')
        if total_seconds < 360:
            time.sleep(round(360 - total_seconds))


if __name__ == "__main__":
    main()
