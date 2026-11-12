# 🏋️ Workout Log & AI Coach

A full-stack web application designed to track gym workouts, automatically calculate training volume, rank personal records (PRs), and provide personalized workout programming powered by **Google Gemini AI**. *(Includes the original Python CLI tracker as a legacy tool).*

## ✨ Features
- **Interactive Web Interface:** Clean, responsive UI with automatic Light/Dark mode support.
- **Automated Volume & PR Leaderboard:** Computes total volume per entry (`Sets × Reps × Weight`) and dynamically ranks exercises by max weight lifted.
- **Built-in Gemini AI Coach:** Analyzes your logged workout history to suggest progressive overload routines and answers app navigation questions.
- **Client-Side Privacy & CSV Export:** Stores workout history locally in the browser (`localStorage`) with one-click export to standard `workout.csv` format.
- **Legacy CLI Mode:** Original terminal-based Python logger (`main.py`) included.

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI, Uvicorn, Google GenAI SDK
- **Frontend:** Vanilla HTML5, CSS3, JavaScript

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Koulis1/gym-cli-tracker.git](https://github.com/Koulis1/gym-cli-tracker.git)
   cd gym-cli-tracker