"""
Pemini Girl 9.5.2 - Database Manager
"""

import os
from datetime import datetime
from typing import Optional, List, Dict
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, Boolean, Float, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.pool import QueuePool
import enum

Base = declarative_base()

class UserRoleEnum(str, enum.Enum):
    ADMIN = "admin"
    DEVELOPER = "developer"
    STUDENT = "student"
    GUEST = "guest"

class CodeActionEnum(str, enum.Enum):
    GENERATE = "generate"
    ANALYZE = "analyze"
    OPTIMIZE = "optimize"
    EXPLAIN = "explain"
    TRANSLATE = "translate"
    COMPLETE = "complete"

class PeminiVersionEnum(str, enum.Enum):
    PRO_7_0 = "pemini_pro_7_0"
    GIRL_9_5_2 = "pemini_girl_9_5_2"

class User(Base):
    __tablename__ = "users"
    user_id = Column(String(32), primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    display_name = Column(String(100), nullable=False)
    password_hash = Column(String(256), nullable=True)
    salt = Column(String(64), nullable=True)
    role = Column(String(20), default="developer")
    auth_provider = Column(String(20), default="local")
    preferred_language = Column(String(10), default="ar")
    preferred_theme = Column(String(20), default="dark")
    default_code_language = Column(String(30), default="python")
    profile_picture = Column(String(500), default="")
    bio = Column(Text, default="")
    location = Column(String(100), default="")
    github_username = Column(String(50), default="")
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CodeSnippet(Base):
    __tablename__ = "code_snippets"
    snippet_id = Column(String(32), primary_key=True)
    user_id = Column(String(32), ForeignKey("users.user_id"), nullable=False)
    title = Column(String(200), nullable=False)
    code = Column(Text, nullable=False)
    language = Column(String(30), nullable=False)
    action = Column(String(20), nullable=False)
    prompt = Column(Text, default="")
    explanation = Column(Text, default="")
    is_favorite = Column(Boolean, default=False)
    tags = Column(JSON, default=list)
    confidence_score = Column(Float, nullable=True)
    execution_time_ms = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserSession(Base):
    __tablename__ = "user_sessions"
    session_id = Column(String(64), primary_key=True)
    user_id = Column(String(32), ForeignKey("users.user_id"), nullable=False)
    token = Column(String(500), nullable=False, unique=True)
    refresh_token = Column(String(500), nullable=True)
    ip_address = Column(String(45), default="")
    user_agent = Column(Text, default="")
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)

class VersionSwitch(Base):
    __tablename__ = "version_switches"
    switch_id = Column(String(32), primary_key=True)
    user_id = Column(String(32), ForeignKey("users.user_id"), nullable=False)
    from_version = Column(String(30), nullable=False)
    to_version = Column(String(30), nullable=False)
    migration_notes = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    log_id = Column(String(32), primary_key=True)
    user_id = Column(String(32), ForeignKey("users.user_id"), nullable=False)
    action = Column(String(50), nullable=False)
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(String(32), nullable=True)
    details = Column(JSON, default=dict)
    ip_address = Column(String(45), default="")
    created_at = Column(DateTime, default=datetime.utcnow)

class SystemStats(Base):
    __tablename__ = "system_stats"
    stat_id = Column(Integer, primary_key=True, autoincrement=True)
    total_users = Column(Integer, default=0)
    total_snippets = Column(Integer, default=0)
    total_sessions = Column(Integer, default=0)
    total_generations = Column(Integer, default=0)
    total_analyses = Column(Integer, default=0)
    avg_generation_time_ms = Column(Float, default=0.0)
    avg_confidence_score = Column(Float, default=0.0)
    active_pro_7_0 = Column(Integer, default=0)
    active_girl_9_5_2 = Column(Integer, default=0)
    recorded_at = Column(DateTime, default=datetime.utcnow)

class DatabaseManager:
    def __init__(self, database_url: str = None):
        self.database_url = database_url or os.getenv(
            "DATABASE_URL", "postgresql://pemini:pemini123@localhost:5432/pemini_db"
        )
        self.engine = None
        self.SessionLocal = None
        self._initialize()

    def _initialize(self):
        try:
            self.engine = create_engine(self.database_url, poolclass=QueuePool,
                pool_size=10, max_overflow=20, pool_pre_ping=True, echo=False)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            Base.metadata.create_all(bind=self.engine)
            print(f"Database connected: {self.database_url.split('@')[-1]}")
        except Exception as e:
            print(f"Database connection error: {e}")
            raise

    def get_session(self):
        return self.SessionLocal()

    def create_user(self, user_data: Dict):
        session = self.get_session()
        try:
            user = User(**user_data)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        except Exception as e:
            session.rollback()
            print(f"Error creating user: {e}")
            return None
        finally:
            session.close()

    def get_user_by_id(self, user_id: str):
        session = self.get_session()
        try:
            return session.query(User).filter(User.user_id == user_id).first()
        finally:
            session.close()

    def get_user_by_username(self, username: str):
        session = self.get_session()
        try:
            return session.query(User).filter(User.username == username).first()
        finally:
            session.close()

    def update_user(self, user_id: str, updates: Dict):
        session = self.get_session()
        try:
            from sqlalchemy import update
            session.execute(update(User).where(User.user_id == user_id).values(**updates))
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            return False
        finally:
            session.close()

    def create_snippet(self, snippet_data: Dict):
        session = self.get_session()
        try:
            snippet = CodeSnippet(**snippet_data)
            session.add(snippet)
            session.commit()
            session.refresh(snippet)
            return snippet
        except Exception as e:
            session.rollback()
            return None
        finally:
            session.close()

    def get_user_snippets(self, user_id: str):
        session = self.get_session()
        try:
            return session.query(CodeSnippet).filter(CodeSnippet.user_id == user_id).order_by(CodeSnippet.created_at.desc()).all()
        finally:
            session.close()

    def record_version_switch(self, switch_data: Dict):
        session = self.get_session()
        try:
            switch = VersionSwitch(**switch_data)
            session.add(switch)
            session.commit()
            return switch
        except Exception as e:
            session.rollback()
            return None
        finally:
            session.close()

    def log_activity(self, log_data: Dict):
        session = self.get_session()
        try:
            log = ActivityLog(**log_data)
            session.add(log)
            session.commit()
            return log
        except:
            session.rollback()
            return None
        finally:
            session.close()

    def record_system_stats(self):
        session = self.get_session()
        try:
            from sqlalchemy import func
            stats = SystemStats(
                total_users=session.query(User).count(),
                total_snippets=session.query(CodeSnippet).count(),
                total_sessions=session.query(UserSession).filter(UserSession.is_active == True).count(),
                total_generations=session.query(CodeSnippet).filter(CodeSnippet.action == "generate").count(),
                total_analyses=session.query(CodeSnippet).filter(CodeSnippet.action == "analyze").count()
            )
            session.add(stats)
            session.commit()
            return stats
        except:
            session.rollback()
            return None
        finally:
            session.close()

if __name__ == "__main__":
    db = DatabaseManager()
    print("Database Manager initialized")
    print("Tables created: users, code_snippets, user_sessions, version_switches, activity_logs, system_stats")
