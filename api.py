from fastapi import FastAPI
from calculator import calculate_one_rep_max, calculate_optimal_set
import sqlite3

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Connected to API"}


@app.get("/calculate-1rm")
def get_one_rep_max(weight: float, reps: int):
    one_rep_max = calculate_one_rep_max(weight, reps)
    return {"one_rep_max": one_rep_max}


@app.get("/save-workout")
def save_workout(exercise: str, weight: float, reps: int, one_rep_max: float):
    connection = sqlite3.connect("workouts.db")
    cursor = connection.cursor()

    insert = """
    INSERT INTO workout_history (exercise, weight, reps, one_rep_max)
    VALUES (?, ?, ?, ?)
    """

    cursor.execute(insert, (exercise, weight, reps, one_rep_max))

    connection.commit()
    connection.close()

    return {
        "status": "Saved Successfully"
    }


@app.get("/calculate-optimal-set")
def get_optimal_set(weight: float, reps: int, min_reps: int, max_reps: int, has_small_plates: bool):
    best_weight, best_reps = calculate_optimal_set(
        weight, reps, min_reps, max_reps, has_small_plates)

    return {
        "best_weight": best_weight,
        "best_reps": best_reps
    }


@app.get("/history")
def get_workout_history():
    connection = sqlite3.connect("Workouts.db")
    cursor = connection.cursor()

    select = """
    SELECT exercise, weight, reps, one_rep_max, date_time
    FROM workout_history
    ORDER BY date_time DESC
    """

    cursor.execute(select)

    rows = cursor.fetchall()

    connection.close()

    history_table = []
    for row in rows:
        history_table.append({
            "exercise": row[0],
            "weight": row[1],
            "reps": row[2],
            "one_rep_max": row[3],
            "date": row[4]

        })

    return {"history": history_table}
