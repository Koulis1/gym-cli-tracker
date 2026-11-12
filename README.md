# 🏋️ Gym CLI Tracker

A structured Python CLI application designed to track gym workouts, calculate total volume, and analyze personal performance records via CSV data storage.

## ✨ Features
- **Workout Logging:** Record exercise name, sets, reps, and weight.
- **Automated Volume Calculation:** Computes total volume per entry (`Sets * Reps * Weight`).
- **Personal Records Leaderboard:** Reads historical CSV data and ranks exercises based on the heaviest weight lifted (case-insensitive with tie-breaking).
- **Robust Validation:** Input checks to handle string cleanups, positive numbers, and float formatting (commas vs dots).
- **Persistent Storage:** Saves entries automatically in standard UTF-8 `workout.csv` format.

## 🚀 How to Run

1. Clone the repository:
   ```bash
git clone [https://github.com/Koulis1/gym-cli-tracker.git](https://github.com/Koulis1/gym-cli-tracker.git)
cd gym-cli-tracker
