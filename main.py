from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engine, get_db
from tables import Base, DBActivityDate, DBBrowserLog, DBCoCurr, DBSkill, DBUser
from verify import create_user, verify_user

app = FastAPI()
Base.metadata.create_all(bind=engine)


class UserCreate(BaseModel):
    username: str
    password: str


class SkillCreate(BaseModel):
    username: str
    title: str
    difficulty_weight: float


class CoCurrCreate(BaseModel):
    username: str
    event_name: str
    base_type_score: float
    role_multiplier: float


class BrowserLogCreate(BaseModel):
    username: str
    domain: str
    minutes_spent: float


class ActivityCreate(BaseModel):
    username: str


def get_user_or_error(db, username):
    user = db.query(DBUser).filter(DBUser.username == username).first()

    if user:
        return user

    return None


@app.get("/")
def home():
    return {"message": "Student Tracking API Running"}



@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if create_user(db, user.username, user.password):
        return {"status": "success", "message": "User created successfully"}

    return {"status": "error", "message": "User already exists"}


@app.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = verify_user(db, user.username, user.password)

    if not db_user:
        return {
            "status": "error",
            "message": "please use the real credentials that you used on the college portal",
        }

    return {
        "status": "success",
        "message": "Login successful",
        "user_id": db_user.id,
        "username": db_user.username,
    }


@app.post("/skills")
def add_skill(skill: SkillCreate, db: Session = Depends(get_db)):
    if not get_user_or_error(db, skill.username):
        return {"status": "error", "message": "User not found"}

    db.add(DBSkill(**skill.dict()))
    db.commit()
    return {"status": "success", "message": "Skill added"}


@app.post("/cocurricular")
def add_cocurricular(cocurr: CoCurrCreate, db: Session = Depends(get_db)):
    if not get_user_or_error(db, cocurr.username):
        return {"status": "error", "message": "User not found"}

    db.add(DBCoCurr(**cocurr.dict()))
    db.commit()
    return {"status": "success", "message": "Co-curricular added"}


@app.post("/browser-log")
def add_browser_log(log: BrowserLogCreate, db: Session = Depends(get_db)):
    if not get_user_or_error(db, log.username):
        return {"status": "error", "message": "User not found"}

    db.add(DBBrowserLog(**log.dict()))
    db.commit()
    return {"status": "success", "message": "Browser log added"}


@app.post("/activity")
def add_activity(activity: ActivityCreate, db: Session = Depends(get_db)):
    if not get_user_or_error(db, activity.username):
        return {"status": "error", "message": "User not found"}

    db.add(DBActivityDate(username=activity.username))
    db.commit()
    return {"status": "success", "message": "Activity added"}


@app.get("/users/{username}")
@app.get("/students/{username}")
def get_user(username: str, db: Session = Depends(get_db)):
    user = get_user_or_error(db, username)

    if not user:
        return {"status": "error", "message": "User not found"}

    return {
        "username": user.username,
        "marks_scored": user.marks_scored,
        "marks_total": user.marks_total,
        "attendance_percent": user.attendance_percent,
        "ema_history": user.ema_history,
        "skills": [
            {"title": skill.title, "difficulty_weight": skill.difficulty_weight}
            for skill in user.skills
        ],
        "cocurriculars": [
            {
                "event_name": item.event_name,
                "base_type_score": item.base_type_score,
                "role_multiplier": item.role_multiplier,
            }
            for item in user.cocurriculars
        ],
        "browser_logs": [
            {"domain": log.domain, "minutes_spent": log.minutes_spent}
            for log in user.browser_logs
        ],
    }
