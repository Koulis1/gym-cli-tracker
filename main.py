import csv
import os
from datetime import date

FILENAME = "workout.csv"
HEADER = ["Date", "Exercise", "Weight (kg)", "Sets", "Reps", "Volume (kg)"]

MENU = """
What would you like to do?
  1. Add a new entry
  2. Show exercise ranking
  3. Exit
"""


def ask_text(prompt):
    """Prompt until a non-empty string is entered."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty. Please try again.")


def ask_float(prompt):
    """Prompt until a non-negative number is entered."""
    while True:
        raw = input(prompt).strip().replace(",", ".")  # accept "62,5" as well as "62.5"
        try:
            value = float(raw)
            if value >= 0:
                return value
            print("Weight cannot be negative.")
        except ValueError:
            print("Please enter a valid number (e.g. 60 or 62.5).")


def ask_int(prompt):
    """Prompt until a positive integer is entered."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if value > 0:
                return value
            print("Value must be greater than 0.")
        except ValueError:
            print("Please enter a valid whole number (e.g. 10).")


def log_workout():
    """Ask for a new entry and append it to the CSV file."""
    exercise = ask_text("Exercise name: ")
    weight = ask_float("Weight (kg): ")
    sets = ask_int("Number of sets: ")
    reps = ask_int("Reps per set: ")

    today = date.today().isoformat()  # YYYY-MM-DD
    volume = round(sets * reps * weight, 2)  # total volume; round() avoids float artifacts

    file_exists = os.path.isfile(FILENAME)

    # newline="" prevents blank rows on Windows; "a" appends without overwriting
    with open(FILENAME, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:  # write the header only when creating the file
            writer.writerow(HEADER)
        writer.writerow([today, exercise, weight, sets, reps, volume])

    print(f"Saved: {today} | {exercise} | {weight} kg | {sets} sets | {reps} reps | {volume} kg")


def show_ranking():
    """Print exercises ranked from best to worst by the heaviest weight ever lifted."""
    if not os.path.isfile(FILENAME):
        print("No workouts recorded yet.")
        return

    best = {}  # lowercase name -> (display name, max weight)
    with open(FILENAME, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            name = row["Exercise"]
            weight = float(row["Weight (kg)"])
            key = name.lower()  # "Squat" and "squat" count as the same exercise
            if key not in best or weight > best[key][1]:
                best[key] = (name, weight)

    if not best:
        print("No workouts recorded yet.")
        return

    # Heaviest first; ties are broken alphabetically for a stable order
    ranking = sorted(best.values(), key=lambda item: (-item[1], item[0].lower()))
    width = max(len(name) for name, _ in ranking)

    print("Exercise ranking (best to worst, by max weight):")
    for position, (name, weight) in enumerate(ranking, start=1):
        print(f"{position:>2}. {name.ljust(width)}  {weight} kg")


def main():
    actions = {"1": log_workout, "2": show_ranking}  # menu choice -> function

    while True:
        print(MENU)
        choice = input("Choose an option (1-3): ").strip()

        if choice == "3":
            print("Goodbye!")
            break

        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice. Please enter 1, 2 or 3.")


if __name__ == "__main__":
    main()