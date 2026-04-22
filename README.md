# 🧞 Akinator Clone – Probability-Based Guessing Engine [WIP]

## 📖 Project Overview
**Status: Work in Progress (Active Development)**

This project is a terminal-based clone of the popular game "Akinator". It is designed as a dynamic guessing engine that attempts to determine the character the user is thinking of by asking a series of Yes/No questions. 

The core focus of this project is building a clean backend architecture, managing persistent state, and implementing a logical filtering/probability algorithm to narrow down search spaces efficiently.

## 🛠️ Technical Architecture
The application is built using **Python** and follows strict software design principles (**Separation of Concerns**):

* **`akinator.py`**: Contains the core Object-Oriented business logic (the Engine) handling the question-asking flow and character filtering.
* **`database.py`**: A dedicated Data Access Layer handling all interactions with the SQLite database.
* **`seed_data.py`**: A robust initialization script used to populate the database with initial entities (Characters), attributes (Questions), and relationships (Answers).
* **`main.py`**: The entry point that orchestrates the engine and the UI.
* **`game_data.db`**: Persistent **SQLite** database storing the knowledge graph.

## 🧠 Core Engine Logic (Target Architecture)
The final iteration of the engine is designed to move beyond simple binary trees to a fully dynamic, mathematical probability matrix:

* **Spectrum Data Modeling:** A Many-to-Many relational structure mapping `Characters` to `Questions`. Answers are evaluated on a spectrum (e.g., 1.0 = Definitely, 0.5 = Don't Know, 0.0 = Definitely Not).
* **Information Gain (Entropy):** The engine dynamically calculates the variance of unanswered questions. It selects the "Best Split" question—the one closest to dividing the remaining candidate pool perfectly in half ($Score(Q) \approx 0$).
* **Bayesian Fault Tolerance:** To handle user errors, candidates are not instantly eliminated. Instead, their probability score is updated using a penalty factor, allowing them to recover if subsequent answers align.
* **Continuous Learning Engine:** If the engine fails to guess correctly, it prompts the user for the answer, inserts the new `Character` into the database, and maps the current session's answer history to this new entity.

## ⚙️ How to Run Locally

1. **Initialize the Database:**
   Run the seed script to create the tables and populate the initial knowledge base:
   ```sh
   python seed_data.py
   ```

2. **Start the Game:**
   ```sh
   python main.py
   ```

## 🗺️ Future Roadmap
- [ ] Implement the Entropy-based dynamic question selection algorithm.
- [ ] Migrate the core logic to support the Bayesian probability updating model.
- [ ] Build the dynamic database insertion for the "Learning" feature.
- [ ] Transition from CLI to a basic Web API (Flask/FastAPI).
