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
        print(f'{pair} {tour} {event} ЗАГРУЖЕН')


league_nms = ['Кубок Австралии', 'Кубок Австралии', 'Кубок Австралии', 'Чемпионат Англии. Премьер-лига', 'Чемпионат Германии. Бундеслига', 'Чемпионат Испании. Примера', 'Чемпионат России. Премьер-лига', 'Чемпионат Франции. Первая лига', 'Чемпионат Нидерландов. Эредивизи', 'Кубок России', 'Кубок России', 'Чемпионат Аргентины. Примера дивизион', 'Чемпионат Аргентины. Примера дивизион', 'Чемпионат Аргентины. Примера дивизион', 'Чемпионат Швейцарии', 'Чемпионат Италии. Серия А', 'Чемпионат Нидерландов. Эредивизи', 'Чемпионат Англии. Премьер-лига', 'Чемпионат Англии. Премьер-лига', 'Чемпионат Чехии', 'Чемпионат Чехии', 'Чемпионат Чехии', 'Кубок Казахстана', 'Кубок Австралии', 'Кубок Австралии']

tours = ['Уолтер Падбери Резерв А (Торнли)', 'Парк Аргана (Аделаида)', 'Саут Перт Юнайтед (Перт)', 'Тур 30', 'Тур 27', 'Тур 28', 'Тур 22', 'Тур 30', 'Тур 27', 'Путь регионов. 1-й этап. 1/2 финала', 'Путь РПЛ. 1/2 финала', 'Флоренцио Сола (Банфилд)', 'Клаудио Чики Тапиа (Буэнос-Айрес)', 'Стадион имени Эстанислао Лопеса (Санта-Фе)', 'Тур 26', 'Тур 29', 'Тур 28', 'Кинг Пауэр (Лестер)', 'Тур 25', 'УМТ Витковице (Острава)', 'Локотранс Арена (Млада Болеслав)', 'Тур 25', 'Тур 2', 'Рон Дайн Резерв (Камден Юг)', 'Брисбен Абуззо Парк (Брисбен)']

for league_nm, tour in zip(league_nms, tours):
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

    for i in [0, 1, 2, 3]:
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
