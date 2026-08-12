from fastapi import FastAPI
from calculator import calculate_one_rep_max, calculate_optimal_set

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "The API is alive!"}


@app.get("/calculate-1rm")
def get_one_rep_max(weight: float, reps: int):
    one_rep_max = calculate_one_rep_max(weight, reps)

    return {
        "weight_lifted": weight,
        "repetitions": reps,
        "one_rep_max": one_rep_max
    }


@app.get("/calculate-optimal-set")
def get_optimal_set(weight: float, reps: int, min_reps: int, max_reps: int, has_small_plates: bool):
    best_weight, best_reps = calculate_optimal_set(
        weight, reps, min_reps, max_reps, has_small_plates)

    return {
        "best_weight": best_weight,
        "best_reps": best_reps
    }
