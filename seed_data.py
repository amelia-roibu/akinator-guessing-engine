from database import create_connection

def seed():
    conn = create_connection()
    cursor = conn.cursor()

    # stergerea datelor vechi de fiecare data cand se ruleaza codul
    cursor.execute("DELETE FROM answers")
    cursor.execute("DELETE FROM questions")
    cursor.execute("DELETE FROM characters")

    # resetarea contorului automat (secventelor)
    cursor.execute("DELETE FROM sqlite_sequence")

    # inserari in tabel
    cursor.execute("INSERT INTO characters (name) VALUES (?)", ("Elon Musk",))
    id_elon = cursor.lastrowid

    cursor.execute("INSERT INTO characters (name) VALUES (?)", ("Mihai Eminescu",))
    id_eminescu = cursor.lastrowid

    cursor.execute("INSERT INTO questions (text) VALUES (?)", ("Is your character a person from the real world?",))
    id_q_real = cursor.lastrowid

    cursor.execute("INSERT INTO questions (text) VALUES (?)", ("Is your character romanian?",))
    id_q_romanian = cursor.lastrowid

    cursor.execute("INSERT INTO answers (character_id, question_id, value) VALUES (?,?,?)", (id_elon, id_q_real, 1.0))
    cursor.execute("INSERT INTO answers (character_id, question_id, value) VALUES (?,?,?)", (id_elon, id_q_romanian, 0.0))

    cursor.execute("INSERT INTO answers (character_id, question_id, value) VALUES (?,?,?)", (id_eminescu, id_q_real, 1.0))
    cursor.execute("INSERT INTO answers (character_id, question_id, value) VALUES (?,?,?)", (id_eminescu, id_q_romanian, 1.0))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed()