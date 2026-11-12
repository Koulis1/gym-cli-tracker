import os
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from google import genai
from google.genai import types

app = FastAPI()
client = genai.Client()

class WorkoutEntry(BaseModel):
    date: str
    exercise: str
    weight: float
    sets: int
    reps: int
    volume: float

class ChatRequest(BaseModel):
    message: str
    history: List[WorkoutEntry] = []

SYSTEM_INSTRUCTION = """
You are the built-in AI Coach & App Navigation Assistant for 'Workout Log'.

APP NAVIGATION & FEATURES (Use this if the user asks how the app works):
1. Add an entry: Fill in Exercise name, Weight (kg), Sets, and Reps per set. Volume is calculated automatically (Weight × Sets × Reps). Click 'Add entry' or press Enter.
2. Ranking by max weight: Automatically displays personal records (PR - heaviest weight lifted) per exercise, sorted from highest to lowest.
3. History: Displays a table of all logged workouts. Includes a 'Delete' button per row, 'Export CSV' to download data as a spreadsheet, and 'Delete all entries' to wipe everything.
4. Storage: Data is saved automatically in the user's local browser storage.

COACHING RULES (Use this if the user asks for a workout plan, advice, or analysis):
- Base your recommendations STRICTLY on the user's provided workout history (weights, sets, reps, dates).
- Suggest realistic progressive overload (e.g., +2.5 kg or +1–2 reps) based on their actual numbers.
- Identify muscle imbalances if major movement patterns are missing (e.g., heavy chest/triceps volume with no back or leg work).
- Keep responses concise and respond in the exact language the user writes in (default to English).

FORMATTING RULES (STRICT):
- Output PLAIN TEXT ONLY.
- NEVER use LaTeX math formatting (no $$, $, \\text, \\times, \\mathbf, etc.). Write plain math like: 80 kg x 4 sets x 5 reps = 1,600 kg.
- NEVER use Markdown syntax like **bold**, *italics*, or ### headers. Use simple dashes (-) or numbers (1., 2.) for lists and line breaks for readability.
"""

MODELS_TO_TRY = [
    "gemini-3.8-flash",
    "gemini-3.8-flash-lite",
    "gemini-3.5-flash"
]

@app.get("/")
def serve_frontend():
    return FileResponse("workout_logger.html")

@app.post("/api/coach")
def ask_coach(req: ChatRequest):
    if not os.environ.get("GEMINI_API_KEY"):
        raise HTTPException(status_code=500, detail="Server configuration error: Missing GEMINI_API_KEY.")

    recent_workouts = req.history[-30:]
    if recent_workouts:
        workout_summary = "\n".join(
            [f"- {w.date}: {w.exercise} | {w.weight}kg | {w.sets}x{w.reps} (Vol: {w.volume}kg)" for w in recent_workouts]
        )
    else:
        workout_summary = "No workouts recorded yet."

    prompt = f"""User's recent workout history:
{workout_summary}

User message:
{req.message}"""

    last_error = None
    for model_name in MODELS_TO_TRY:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.4,
                ),
            )
            return {"reply": response.text}
        except Exception as e:
            last_error = str(e)
            if "503" in last_error or "429" in last_error or "404" in last_error:
                continue
            break

    raise HTTPException(
        status_code=503,
        detail="AI Coach is experiencing high traffic right now. Please try again in a few seconds."
    )