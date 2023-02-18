def create_events():
    return """
    CREATE TABLE IF NOT EXISTS events (
      event_id INTEGER PRIMARY KEY AUTOINCREMENT,
      event_nm TEXT NOT NULL,
      event_vl TEXT NOT NULL,
      event_sgn TEXT
    )
    """


def create_coeffs():
    return """
    CREATE TABLE IF NOT EXISTS game_coeffs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      game_id INTEGER,
      time TEXT,
      cntry_nm TEXT,
      league_id INTEGER,
      league_nm TEXT,
      sport_nm TEXT,
      tour INTEGER,
      opponent_a TEXT,
      opponent_b TEXT,
      event_id INTEGER NOT NULL,
      coeff REAL,
      FOREIGN KEY(event_id) REFERENCES events(event_id)
    )
    """


def insert_events():
    return """
    insert into events (event_nm, event_vl, event_sgn)
    values ('1x2', '1', NULL),
    ('1x2', 'x', NULL),
    ('1x2', '2', NULL),
    ('Двойной шанс', '1x', NULL),
    ('Двойной шанс', '12', NULL),
    ('Двойной шанс', '2x', NULL),
    ('Тотал', '0', 'Б'),
    ('Тотал', '0.5', 'Б'),
    ('Тотал', '1', 'Б'),
    ('Тотал', '1.5', 'Б'),
    ('Тотал', '2', 'Б'),
    ('Тотал', '2.5', 'Б'),
    ('Тотал', '3', 'Б'),
    ('Тотал', '3.5', 'Б'),
    ('Тотал', '4', 'Б'),
    ('Тотал', '4.5', 'Б'),
    ('Тотал', '5', 'Б'),
    ('Тотал', '5.5', 'Б'),
    ('Тотал', '6', 'Б'),
    ('Тотал', '6.5', 'Б'),
    ('Тотал', '7', 'Б'),
    ('Тотал', '7.5', 'Б'),
    ('Тотал', '8', 'Б'),
    ('Тотал', '8.5', 'Б'),
    ('Тотал', '9', 'Б'),
    ('Тотал', '9.5', 'Б'),
    ('Тотал', '10', 'Б'),
    ('Тотал', '10.5', 'Б'),
    ('Тотал', '11', 'Б'),
    ('Тотал', '11.5', 'Б'),
    ('Тотал', '12', 'Б'),
    ('Тотал', '12.5', 'Б'),
    ('Тотал', '13', 'Б'),
    ('Тотал', '13.5', 'Б'),
    ('Тотал', '14', 'Б'),
    ('Тотал', '14.5', 'Б'),
    ('Тотал', '15', 'Б'),
    ('Тотал', '15.5', 'Б'),
    ('Тотал', '16', 'Б'),
    ('Тотал', '16.5', 'Б'),
    ('Тотал', '17', 'Б'),
    ('Тотал', '17.5', 'Б'),
    ('Тотал', '18', 'Б'),
    ('Тотал', '18.5', 'Б'),
    ('Тотал', '0', 'М'),
    ('Тотал', '0.5', 'М'),
    ('Тотал', '1', 'М'),
    ('Тотал', '1.5', 'М'),
    ('Тотал', '2', 'М'),
    ('Тотал', '2.5', 'М'),
    ('Тотал', '3', 'М'),
    ('Тотал', '3.5', 'М'),
    ('Тотал', '4', 'М'),
    ('Тотал', '4.5', 'М'),
    ('Тотал', '5', 'М'),
    ('Тотал', '5.5', 'М'),
    ('Тотал', '6', 'М'),
    ('Тотал', '6.5', 'М'),
    ('Тотал', '7', 'М'),
    ('Тотал', '7.5', 'М'),
    ('Тотал', '8', 'М'),
    ('Тотал', '8.5', 'М'),
    ('Тотал', '9', 'М'),
    ('Тотал', '9.5', 'М'),
    ('Тотал', '10', 'М'),
    ('Тотал', '10.5', 'М'),
    ('Тотал', '11', 'М'),
    ('Тотал', '11.5', 'М'),
    ('Тотал', '12', 'М'),
    ('Тотал', '12.5', 'М'),
    ('Тотал', '13', 'М'),
    ('Тотал', '13.5', 'М'),
    ('Тотал', '14', 'М'),
    ('Тотал', '14.5', 'М'),
    ('Тотал', '15', 'М'),
    ('Тотал', '15.5', 'М'),
    ('Тотал', '16', 'М'),
    ('Тотал', '16.5', 'М'),
    ('Тотал', '17', 'М'),
    ('Тотал', '17.5', 'М'),
    ('Тотал', '18.0', 'М'),
    ('Тотал', '18.5', 'М'),
    ('Тотал', '19', 'М'),
    ('Тотал', '19.5', 'М'),
    ('Тотал', '20', 'М'),
    ('Фора', '5', '1'),
    ('Фора', '4.5', '1'),
    ('Фора', '4', '1'),
    ('Фора', '3.5', '1'),
    ('Фора', '3', '1'),
    ('Фора', '2.5', '1'),
    ('Фора', '2', '1'),
    ('Фора', '1.5', '1'),
    ('Фора', '1', '1'),
    ('Фора', '0.5', '1'),
    ('Фора', '0', '1'),
    ('Фора', '-0.5', '1'),
    ('Фора', '-1', '1'),
    ('Фора', '-1.5', '1'),
    ('Фора', '-2', '1'),
    ('Фора', '-2.5', '1'),
    ('Фора', '-3', '1'),
    ('Фора', '-3.5', '1'),
    ('Фора', '-4', '1'),
    ('Фора', '-4.5', '1'),
    ('Фора', '-5', '1'),
    ('Фора', '5', '2'),
    ('Фора', '4.5', '2'),
    ('Фора', '4', '2'),
    ('Фора', '3.5', '2'),
    ('Фора', '3', '2'),
    ('Фора', '2.5', '2'),
    ('Фора', '2', '2'),
    ('Фора', '1.5', '2'),
    ('Фора', '1', '2'),
    ('Фора', '0.5', '2'),
    ('Фора', '0', '2'),
    ('Фора', '-0.5', '2'),
    ('Фора', '-1', '2'),
    ('Фора', '-1.5', '2'),
    ('Фора', '-2', '2'),
    ('Фора', '-2.5', '2'),
    ('Фора', '-3', '2'),
    ('Фора', '-3.5', '2'),
    ('Фора', '-4', '2'),
    ('Фора', '-4.5', '2'),
    ('Фора', '-5', '2')
    """