import sqlite3


def create_database():
    connection = sqlite3.connect("workouts.db")

    cursor = connection.cursor()

    create_table = """
    CREATE TABLE IF NOT EXISTS workout_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exercise TEXT NOT NULL,
        weight REAL NOT NULL,
        reps INTEGER NOT NULL,
        one_rep_max REAL NOT NULL,
        date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    cursor.execute(create_table)
    connection.commit()

    connection.close()


if __name__ == "__main__":
    create_database()
