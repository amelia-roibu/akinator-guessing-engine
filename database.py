import sqlite3

def create_connection():
    # se conecteaza la fisier sau il creeaza daca nu exista
    conn = sqlite3.connect('game_data.db')
    return conn

def initialize_db():
    conn = create_connection()
    cursor = conn.cursor()

    # crearea tabelelor

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            times_played INTEGER DEFAULT 0
        )
    ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL UNIQUE
            )
        ''')

    cursor.execute('''
                CREATE TABLE IF NOT EXISTS answers (
                    character_id INTEGER,
                    question_id INTEGER,
                    value REAL,
                    FOREIGN KEY (character_id) REFERENCES characters(id),
                    FOREIGN KEY (question_id) REFERENCES questions(id),
                    PRIMARY KEY (character_id, question_id)
                )
            ''')

    conn.commit()
    conn.close()
    print('Data Base initialised successfully!')

# asta face ca functia sa ruleze doar cand dau run la acest fisier
# altfel, cand de exemplu dau import la database in alt fisier,
# o sa ruleze din nou si din nou functia initialize_db()
if __name__ == "__main__":
    initialize_db()