"""
database.py
-----------
Handles everything SQLite related:
  - Creating the database and all tables on first run
  - User registration and login
  - Saving / fetching prediction history
  - Saving / fetching health metrics
  - Patient profile storage
"""

import sqlite3
import os
import json
import hashlib
import hmac
from datetime import datetime
from contextlib import contextmanager

DB_PATH = os.path.join("data", "mediscan.db")


# ── Connection ─────────────────────────────────────────────────────────────

@contextmanager
def _connect():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ── Initialise all tables ──────────────────────────────────────────────────

def init_db():
    """Create all tables on first run. Called once at app startup."""
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                username      TEXT UNIQUE NOT NULL,
                email         TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name     TEXT,
                created_at    TEXT NOT NULL,
                last_login    TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS patient_profiles (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER UNIQUE NOT NULL REFERENCES users(id),
                age         INTEGER,
                gender      TEXT,
                weight_kg   REAL,
                height_cm   REAL,
                blood_group TEXT,
                updated_at  TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS prediction_history (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL REFERENCES users(id),
                disease     TEXT NOT NULL,
                confidence  REAL NOT NULL,
                risk_score  REAL,
                risk_level  TEXT,
                symptoms    TEXT,
                bmi         REAL,
                temperature REAL,
                created_at  TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS health_metrics (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id       INTEGER NOT NULL REFERENCES users(id),
                bmi           REAL,
                temperature   REAL,
                symptom_count INTEGER,
                risk_score    REAL,
                recorded_at   TEXT NOT NULL
            )
        """)


# ── Password helpers ───────────────────────────────────────────────────────

def _hash_password(password: str) -> str:
    salt = os.urandom(32).hex()
    key  = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 260_000).hex()
    return f"{salt}${key}"

def _verify_password(password: str, stored: str) -> bool:
    try:
        salt, key = stored.split("$")
        candidate = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 260_000).hex()
        return hmac.compare_digest(candidate, key)
    except Exception:
        return False


# ── Users ──────────────────────────────────────────────────────────────────

def create_user(username: str, email: str, password: str, full_name: str = "") -> tuple:
    """Register a new user. Returns (success: bool, message: str)."""
    with _connect() as conn:
        if conn.execute("SELECT 1 FROM users WHERE username=?", (username.lower(),)).fetchone():
            return False, "Username already taken."
        if conn.execute("SELECT 1 FROM users WHERE email=?", (email.lower(),)).fetchone():
            return False, "Email already registered."
        conn.execute(
            "INSERT INTO users (username, email, password_hash, full_name, created_at) VALUES (?,?,?,?,?)",
            (username.lower(), email.lower(), _hash_password(password), full_name, datetime.now().isoformat())
        )
    return True, "Account created successfully!"


def verify_login(identifier: str, password: str) -> tuple:
    """Check credentials. Returns (success: bool, message: str, user: dict|None)."""
    with _connect() as conn:
        field = "email" if "@" in identifier else "username"
        row   = conn.execute(f"SELECT * FROM users WHERE {field}=?", (identifier.lower(),)).fetchone()
        if not row:
            return False, "No account found with that username or email.", None
        user = dict(row)
        if not _verify_password(password, user["password_hash"]):
            return False, "Incorrect password.", None
        conn.execute("UPDATE users SET last_login=? WHERE id=?", (datetime.now().isoformat(), user["id"]))
    return True, f"Welcome back, {user.get('full_name') or user['username']}!", user


def get_user_by_id(user_id: int) -> dict:
    with _connect() as conn:
        row = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
        return dict(row) if row else None


# ── Patient profile ────────────────────────────────────────────────────────

def save_profile(user_id: int, age: int, gender: str, weight_kg: float,
                 height_cm: float, blood_group: str = ""):
    now = datetime.now().isoformat()
    with _connect() as conn:
        exists = conn.execute("SELECT 1 FROM patient_profiles WHERE user_id=?", (user_id,)).fetchone()
        if exists:
            conn.execute(
                "UPDATE patient_profiles SET age=?,gender=?,weight_kg=?,height_cm=?,blood_group=?,updated_at=? WHERE user_id=?",
                (age, gender, weight_kg, height_cm, blood_group, now, user_id)
            )
        else:
            conn.execute(
                "INSERT INTO patient_profiles (user_id,age,gender,weight_kg,height_cm,blood_group,updated_at) VALUES (?,?,?,?,?,?,?)",
                (user_id, age, gender, weight_kg, height_cm, blood_group, now)
            )

def get_profile(user_id: int) -> dict:
    with _connect() as conn:
        row = conn.execute("SELECT * FROM patient_profiles WHERE user_id=?", (user_id,)).fetchone()
        return dict(row) if row else None


# ── Prediction history ─────────────────────────────────────────────────────

def save_prediction(user_id: int, disease: str, confidence: float, risk_score: float,
                    risk_level: str, symptoms: list, bmi: float, temperature: float):
    with _connect() as conn:
        conn.execute(
            "INSERT INTO prediction_history (user_id,disease,confidence,risk_score,risk_level,symptoms,bmi,temperature,created_at) VALUES (?,?,?,?,?,?,?,?,?)",
            (user_id, disease, confidence, risk_score, risk_level,
             json.dumps(symptoms), bmi, temperature, datetime.now().isoformat())
        )

def get_predictions(user_id: int, limit: int = 20) -> list:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM prediction_history WHERE user_id=? ORDER BY created_at DESC LIMIT ?",
            (user_id, limit)
        ).fetchall()
    results = []
    for row in rows:
        r = dict(row)
        try:    r["symptoms"] = json.loads(r["symptoms"])
        except: r["symptoms"] = []
        results.append(r)
    return results


# ── Health metrics ─────────────────────────────────────────────────────────

def save_metric(user_id: int, bmi: float, temperature: float,
                symptom_count: int, risk_score: float):
    with _connect() as conn:
        conn.execute(
            "INSERT INTO health_metrics (user_id,bmi,temperature,symptom_count,risk_score,recorded_at) VALUES (?,?,?,?,?,?)",
            (user_id, bmi, temperature, symptom_count, risk_score, datetime.now().isoformat())
        )

def get_metrics(user_id: int, limit: int = 30) -> list:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM health_metrics WHERE user_id=? ORDER BY recorded_at DESC LIMIT ?",
            (user_id, limit)
        ).fetchall()
    return [dict(r) for r in rows]
