import hashlib
import sqlite3
from typing import Optional

class DatabaseManager:
    """Gestiona la libreta de memoria para no repetir ofertas laborales."""

    def __init__(self, db_path: str = "jobs_tracker.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        """Pieza 1: Dibuja la tabla en la libreta si no existe."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS seen_jobs (
                    job_hash TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    company TEXT,
                    location TEXT,
                    source TEXT,
                    job_url TEXT NOT NULL,
                    seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    @staticmethod
    def generate_hash(title: str, company: Optional[str], job_url: str) -> str:
        """Pieza 2: Convierte los datos del empleo en una huella digital única."""
        clean_company = (company or "").lower().strip()
        raw_identity = f"{title.lower().strip()}|{clean_company}|{job_url.strip()}"
        return hashlib.sha256(raw_identity.encode("utf-8")).hexdigest()

    def is_new_job(self, job_hash: str) -> bool:
        """Pieza 3: Pregunta a la libreta: ¿Esta huella ya existe?"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM seen_jobs WHERE job_hash = ?", (job_hash,))
            return cursor.fetchone() is None

    def save_job(self, job_hash: str, title: str, company: str, location: str, source: str, job_url: str) -> None:
        """Pieza 4: Escribe la nueva oferta en la libreta para recordarla."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO seen_jobs (job_hash, title, company, location, source, job_url)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (job_hash, title, company, location, source, job_url))
            conn.commit()