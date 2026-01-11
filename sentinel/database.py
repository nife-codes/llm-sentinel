import sqlite3
from datetime import datetime
from . import config

class DecisionLogger:
    def __init__(self):
        self.db_path = config.DB_PATH
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS decisions (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                prompt TEXT,
                cached INTEGER,
                reason TEXT,
                similarity REAL,
                tokens INTEGER,
                cost_saved REAL
            )
        """)
        conn.commit()
        conn.close()
    
    def log(self, prompt: str, cached: bool, reason: str, similarity: float = None, tokens: int = 0, cost_saved: float = 0.0):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            "INSERT INTO decisions VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)",
            (datetime.now().isoformat(), prompt, 1 if cached else 0, reason, similarity, tokens, cost_saved)
        )
        conn.commit()
        conn.close()
    
    def get_metrics(self) -> dict:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        total = c.execute("SELECT COUNT(*) FROM decisions").fetchone()[0]
        if total == 0:
            conn.close()
            return {"total_requests": 0, "cache_hits": 0, "cache_hit_rate": 0.0, "total_cost_saved": 0.0}
        
        hits = c.execute("SELECT COUNT(*) FROM decisions WHERE cached=1").fetchone()[0]
        cost_saved = c.execute("SELECT SUM(cost_saved) FROM decisions").fetchone()[0] or 0.0
        
        conn.close()
        
        return {
            "total_requests": total,
            "cache_hits": hits,
            "cache_hit_rate": hits / total,
            "total_cost_saved": round(cost_saved, 2),
        }