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
      opponent_a TEXT,
      opponent_b TEXT,
      event_id INTEGER NOT NULL,
      coeff REAL,
      FOREIGN KEY(event_id) REFERENCES events(event_id)
    )
    """
