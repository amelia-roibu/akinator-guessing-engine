from database import create_connection

class AkinatorEngine:
    def __init__(self):
        # structuri python de tip liste / dictionare pentru injectarea datelor din baza de date
        self.candidates = []
        self.questions = []
        self.answers = {} # dictionar
        self.asked_questions = [] # id-urile intrebarilor deja puse

        self._load_data()

    def _load_data(self):
        conn = create_connection()
        cursor = conn.cursor()

        # fetch personaje
        cursor.execute("SELECT id, name FROM characters")
        rows = cursor.fetchall() # => o lista de tupluri [(1, 'Elon'), (2, 'Eminescu')]
        for row in rows: # fiecare row este un tuplu de personaj
            object = {
                'id': row[0],
                'name': row[1],
                'probability': 1.0 # toti candidatii incep cu sanse egale
            }
            self.candidates.append(object)

        # fetch intrebari
        cursor.execute("SELECT id, text FROM questions")
        rows = cursor.fetchall()
        for row in rows:
            object = {
                'id': row[0],
                'text': row[1]
            }
            self.questions.append(object)

        # fetch raspunsuri
        cursor.execute("SELECT character_id, question_id, value FROM answers")
        rows = cursor.fetchall()
        for row in rows:
            character_id = row[0]
            question_id = row[1]
            value = row[2]

            if character_id not in self.answers:
                self.answers[character_id] = {}

            self.answers[character_id][question_id] = value

        conn.close()

    def get_next_question(self):
        best_question = None
        minimal_difference = 1.0

        # calculam media raspunsurilor, pentru a vedea care dintre ele elimina cei mai multi candidati
        # folosim media ponderata si apoi facem diferenta in modul cu 0.5
        total_probability = 0
        for candidate in self.candidates:
            total_probability += candidate['probability']

        if total_probability == 0:
            return None

        for question in self.questions:
            if question['id'] not in self.asked_questions:
                current_weighted_sum = 0 # suma pentru media ponderata

                for candidate in self.candidates:
                    candidate_id = candidate['id']
                    question_id = question['id']

                    value = 0.5
                    if candidate_id in self.answers and question_id in self.answers[candidate_id]:
                        value = self.answers[candidate_id][question_id]

                    current_weighted_sum += value * candidate['probability'] # valoarea intrebarii * probabilitatea sa fie acela personajul

                average = current_weighted_sum / total_probability
                difference = abs(0.5 - average)
                if difference < minimal_difference:
                    minimal_difference = difference
                    best_question = question

        return best_question

    def update_probabilities(self, question_id, user_answer):
        # user_answer poate fi 1.0, 0.75, 0.5, 0.25, 0.0
        for candidate in self.candidates:
            candidate_id = candidate['id']
            expected_answer = 0.5 # initializat cu informatia neutra in cazul in care nu stim nimic despre personaj din baza de date
            if candidate_id in self.answers and question_id in self.answers[candidate_id]:
                expected_answer = self.answers[candidate_id][question_id]

            difference = abs(user_answer - expected_answer)
            match_score = 1.0 - (0.8 * difference)
            # scorul de potrivire
            # 0 -> probabilitatea ramane neschimbata
            # 1 -> probabilitatea scade drastic
            # 0.8 este factorul de severitate in formula 1.0 - (0.8 * difference)

            candidate['probability'] = candidate['probability'] * match_score

    def get_top_guess(self):
        # sortarea candidatilor in ordine descrescatoare, in functie de probabilitati
        sorted_candidates = sorted(self.candidates, key=lambda x: x['probability'], reverse=True)

        if not sorted_candidates:
            return None, 0.0

        best_candidate = sorted_candidates[0]
        return best_candidate, best_candidate['probability']