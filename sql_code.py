def create_events():
    return """
    CREATE TABLE IF NOT EXISTS events (
      event_id INTEGER PRIMARY KEY AUTOINCREMENT,
      event_nm TEXT NOT NULL,
      event_vl TEXT NOT NULL,
      event_sgn TEXT
    )
    """


def create_football_coeffs():
    return """
    CREATE TABLE IF NOT EXISTS coeffs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      time TEXT,
      cntry_nm TEXT,
      league_nm TEXT,
      tour TEXT,
      opponent_a TEXT,
      opponent_b TEXT,
      event_nm TEXT,
      event_vl TEXT,
      coeff REAL
    )
    """


def create_tennis_coeffs():
    return """
    CREATE TABLE IF NOT EXISTS coeffs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      time TEXT,
      cntry_nm TEXT,
      league_nm TEXT,
      tour TEXT,
      opponent_a TEXT,
      opponent_b TEXT,
      event_nm TEXT,
      event_vl TEXT,
      coeff REAL
    )
    """
