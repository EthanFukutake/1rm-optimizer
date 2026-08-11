# CONSTANTS
BRZYCKI_NUMERATOR = 36
BRZYCKI_DENOMINATOR = 37
EPLEY_DIVISOR = 30
STANDARD_PLATE_JUMP = 5.0
MICRO_PLATE_JUMP = 2.5

# Calculate the estimated one-rep max based on weight lifted and reps performed


def calculate_one_rep_max(weight: float, reps: int) -> float:
    # FIX: Guard clauses ensure mathematical boundaries are respected regardless of how the function is called
    if weight <= 0:
        raise ValueError("Weight must be greater than zero.")
    if reps <= 0:
        raise ValueError("Reps must be at least 1.")

    if reps <= 5:
        # Protects against ZeroDivisionError if the formula threshold or constants are ever modified
        if reps >= BRZYCKI_DENOMINATOR:
            raise ValueError(
                f"Brzycki formula is invalid for reps >= {BRZYCKI_DENOMINATOR}")
        # Brzycki formula - more accurate for low reps
        return weight * (BRZYCKI_NUMERATOR / (BRZYCKI_DENOMINATOR - reps))
    else:
        # Epley formula - better for higher reps
        return weight * (1 + (reps / EPLEY_DIVISOR))

# Calculate the weight to lift for a given number of reps based on a target 1RM


def calculate_weight_for_reps(target_one_rep_max: float, reps: int) -> float:
    # FIX: Consistent validation for inverse calculations
    if target_one_rep_max <= 0:
        raise ValueError("Target 1RM must be greater than zero.")
    if reps <= 0:
        raise ValueError("Reps must be at least 1.")

    if reps <= 5:
        return target_one_rep_max * ((BRZYCKI_DENOMINATOR - reps) / BRZYCKI_NUMERATOR)
    else:
        return target_one_rep_max / (1 + (reps / EPLEY_DIVISOR))

# Calculate the optimal weight and reps for the next set based on user input and available plate increments


def calculate_optimal_set(weight: float, reps: int, min_reps: int, max_reps: int, has_small_plates: bool) -> tuple[float, int]:
    if not (1 <= reps <= 20):
        raise ValueError("Reps must be between 1 and 20")

    # Determine smallest available weight increment
    smallest_plate = MICRO_PLATE_JUMP if has_small_plates else STANDARD_PLATE_JUMP

    one_rep_max = calculate_one_rep_max(weight, reps)

    new_rep_max = one_rep_max + 1

    best_weight = 0.0
    best_reps = 0
    smallest_difference = float('inf')

    # Try every rep count in the preferred range to find the closest match
    for r in range(min_reps, max_reps + 1):
        raw_weight = calculate_weight_for_reps(new_rep_max, r)
        rounded_weight = round(raw_weight / smallest_plate) * smallest_plate

        test_1rm = calculate_one_rep_max(rounded_weight, r)
        difference = abs(test_1rm - new_rep_max)

        if difference < smallest_difference:
            smallest_difference = difference
            best_weight = rounded_weight
            best_reps = r

    if best_weight == weight and best_reps == reps:
        print("\nNo better set found within the preferred rep range. Consider adjusting your rep range or using smaller plates if available.")

    return best_weight, best_reps


# Validate user input for numeric values with optional min/max constraints
def get_numeric_input(prompt: str, cast_type: type, min_val: float = None, max_val: float = None):
    """Handles all numeric user input with built-in validation."""
    while True:
        try:
            value = cast_type(input(prompt))
            if (min_val is None or value >= min_val) and (max_val is None or value <= max_val):
                return value

            # Dynamic error messaging based on constraints
            if min_val is not None and max_val is not None:
                print(
                    f"Invalid input. Please enter a number between {min_val} and {max_val}.")
            elif min_val is not None:
                print(
                    f"Invalid input. Please enter a number greater than or equal to {min_val}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def main():
    print("1RM Calculator and Optimizer")
    print("----------------------------")

    # Get user input for weight, reps, and preferred rep range
    weight = get_numeric_input(
        "Enter the weight lifted (in lbs): ", float, min_val=1)
    reps = get_numeric_input(
        "Enter the number of repetitions performed (1-20): ", int, min_val=1, max_val=20)
    min_reps = get_numeric_input(
        "Enter the minimum number for your preferred rep range (1-19): ", int, min_val=1, max_val=19)
    max_reps = get_numeric_input(
        f"Enter the maximum number for your preferred rep range ({min_reps + 1}-20): ", int, min_val=min_reps + 1, max_val=20)

    # Check if the user has 1.25lb plates available for more precise weight adjustments
    while True:
        answer = input("Do you have 1.25lb plates? (Y/N): ").strip().upper()
        if answer in ("Y", "N"):
            has_small_plates = (answer == "Y")
            break

        print("Invalid input. Please enter Y or N.")

    best_weight, best_reps = calculate_optimal_set(
        weight, reps, min_reps, max_reps, has_small_plates)

    print(
        f"\nYour estimated 1RM is: {calculate_one_rep_max(weight, reps)} lbs.")
    print(f"\nNext time try {best_weight} lbs for {best_reps} reps.")


if __name__ == "__main__":
    main()
