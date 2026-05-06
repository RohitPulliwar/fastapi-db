from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class DBUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    enrollment_number = Column(String, unique=True, index=True)
    password_hash = Column(String)
    marks_scored = Column(Float, default=0.0)
    marks_total = Column(Float, default=100.0)
    attendance_percent = Column(Float, default=0.0)
    ema_history = Column(JSON, default=lambda: [50.0])

    skills = relationship("DBSkill", back_populates="user", cascade="all, delete")
    cocurriculars = relationship("DBCoCurr", back_populates="user", cascade="all, delete")
    browser_logs = relationship("DBBrowserLog", back_populates="user", cascade="all, delete")
    activity_dates = relationship("DBActivityDate", back_populates="user", cascade="all, delete")


class DBSkill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, ForeignKey("users.username"))
    title = Column(String)
    difficulty_weight = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("DBUser", back_populates="skills")


class DBCoCurr(Base):
    __tablename__ = "cocurriculars"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, ForeignKey("users.username"))
    event_name = Column(String)
    base_type_score = Column(Float)
    role_multiplier = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("DBUser", back_populates="cocurriculars")


class DBBrowserLog(Base):
    __tablename__ = "browser_logs"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, ForeignKey("users.username"))
    domain = Column(String)
    minutes_spent = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("DBUser", back_populates="browser_logs")


class DBActivityDate(Base):
    __tablename__ = "activity_dates"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, ForeignKey("users.username"))
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("DBUser", back_populates="activity_dates")
