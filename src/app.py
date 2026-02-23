"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Team basketball practice and inter-school matches",
        "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["liam@mergington.edu", "ava@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Swim training, stroke techniques, and fitness",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["noah@mergington.edu", "mia@mergington.edu"]
    },
    "Drama Club": {
        "description": "Acting workshops and school theater performances",
        "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["lucas@mergington.edu", "harper@mergington.edu"]
    },
    "Art Studio": {
        "description": "Drawing, painting, and mixed-media art projects",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["amelia@mergington.edu", "evelyn@mergington.edu"]
    },
    "Debate Society": {
        "description": "Practice public speaking and structured debates",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["james@mergington.edu", "charlotte@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Explore scientific concepts and compete in STEM challenges",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["benjamin@mergington.edu", "isabella@mergington.edu"]
    }
}


class SignupRequest(BaseModel):
    email: str


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, payload: SignupRequest):
    """Sign up a student for an activity"""
    email = payload.email.strip().lower()

    activity = activities.get(activity_name)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # 既存参加者を正規化して重複チェック
    if any(p.strip().lower() == email for p in activity["participants"]):
        raise HTTPException(status_code=409, detail="Student already signed up")

    activity["participants"].append(email)
    return {"message": "Signed up successfully"}


@app.delete("/activities/{activity_name}/participants")
def unregister_participant(activity_name: str, email: str):
    """Unregister a student from an activity"""
    normalized_email = email.strip().lower()

    activity = activities.get(activity_name)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    participant_index = next(
        (index for index, participant in enumerate(activity["participants"])
         if participant.strip().lower() == normalized_email),
        None,
    )

    if participant_index is None:
        raise HTTPException(status_code=404, detail="Participant not found in activity")

    removed_participant = activity["participants"].pop(participant_index)
    return {"message": f"{removed_participant} has been unregistered"}
