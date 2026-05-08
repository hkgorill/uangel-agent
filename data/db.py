"""SQLite 데이터 저장 — SQLAlchemy ORM."""

from contextlib import contextmanager
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///data/uangel.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=True)
Base = declarative_base()


class InterventionLog(Base):
    __tablename__ = "intervention_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(64), nullable=False, index=True)
    component = Column(String(64), nullable=False)
    utterance = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserProfile(Base):
    __tablename__ = "user_profile"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(64), nullable=False, index=True)
    component = Column(String(64), nullable=False)
    weight = Column(Float, default=0.5)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class FeedbackLog(Base):
    __tablename__ = "feedback_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    intervention_log_id = Column(Integer, nullable=False)
    user_id = Column(String(64), nullable=False, index=True)
    component = Column(String(64), nullable=False)
    reaction = Column(String(64), nullable=False)
    score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)


@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
