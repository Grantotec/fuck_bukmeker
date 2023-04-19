import os
from sqlite3 import connect
import pandas as pd
import matplotlib.pyplot as plt


def plot_game_data(game_data, league_nm, tour, pair):
    # Определяем события
    events = game_data.events.unique()
    # Проходимся по каждому событию
    for event in events:
        # Берем событие
        event_data = game_data[game_data.events == event]
        event_data.plot('time', 'coeff', rot=90)
        plt.title(f'{pair} {tour} {event}')
        plt.xlabel('Время')
        plt.ylabel('Кэфы')

        # Собираем путь будующего файла
        path_nm = r'/Users/nelson/PycharmProjects/fuck_bukmeker/Graphics'
        file_nm = f'/{league_nm}/{tour}/{pair}/{event}.jpg'
        save_path = path_nm + file_nm

        # Проверяем, существует ли папка, указанная в пути
        if not os.path.exists(os.path.dirname(save_path)):
            # Создаем папку, если она не существует
            os.makedirs(os.path.dirname(save_path))

        # Сохраняем график в папку
        plt.savefig(save_path, bbox_inches='tight')
        plt.close('all')

leagues_list = [('Чемпионат России. Премьер-лига', 'None'),
                ('Чемпионат Германии. 2-я Бундеслига', 'Тур 26'),
                ('Чемпионат Бельгии. Премьер-лига', 'Тур 32'),
                ('Чемпионат Шотландии. Премьер-лига', 'Тур 31'),
                ('Кубок Чехии', '1/2 финала'),
                ('Чемпионат Швеции. Суперэттан', 'Тур 1'),
                ('Чемпионат Шотландии. Чемпионшип', 'Тур 28'),
                ('Чемпионат Нидерландов. Эредивизи', 'Тур 27'),
                ('Чемпионат Испании. Примера', 'None'),
                ('Чемпионат России. 1-я лига', 'Тур 27'),
                ('Чемпионат Италии. Серия B', 'Тур 29'),
                ('Чемпионат Швеции. Аллсвенскан', 'None'),
                ('Чемпионат Франции. Первая лига', 'Тур 30'),
                ('Чемпионат Италии. Серия B', 'Тур 32'),
                ('Чемпионат Испании. Второй дивизион', 'Тур 36'),
                ('Чемпионат Шотландии. Чемпионшип', 'Тур 33'),
                ('Чемпионат Франции. Первая лига', 'None'),
                ('Чемпионат Европы 2024', 'Квалификация. Групповой этап. Тур 2. Группа G'),
                ('Чемпионат Швеции. Аллсвенскан', 'Тур 4'),
                ('Чемпионат Швеции. Аллсвенскан', 'Бравида (Гётеборг)')]

for league_nm, tour in leagues_list:
    print(league_nm, tour)
    sql = f"""

    SELECT

        *

    FROM coeffs

    WHERE 1=1
        and league_nm = '{league_nm}'
        and tour LIKE "%{tour}%"
    """

    cons = list()

    for i in [0, 1, 2, 3, 4, 5, 6, 7]:
        db_name = f'archiv/football_{i}.db'
        print(db_name)
        con = connect(db_name)
        cons.append(pd.read_sql(sql, con))
        con.close()

    df = pd.concat(cons)
    del cons
    print(f'Данные загружены. {len(df)} строк.')

    df['pairs'] = df['opponent_a'] + ' - ' + df['opponent_b']
    df['events'] = df['event_nm'] + '[' + df['event_vl'] + ']'
    df.drop(columns=['opponent_a', 'opponent_b', 'event_nm', 'event_vl'], inplace=True)

    # Определяем игры
    pairs = list(df.pairs.unique())
    # Проходимся по играм
    for pair in pairs:
        print('-' * 10, pair, '-' * 10)

        # Берем конретную игру
        game_data = df[df.pairs == pair]

        # Строим график и сохраняем в папку
        plot_game_data(game_data, league_nm, tour, pair)

    del df,
