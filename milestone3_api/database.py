import sqlite3
import datetime

DB_NAME = "jobcheck.db"

def init_db():
    """Initialize the database tables."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Table: Prediction Logs
    c.execute('''CREATE TABLE IF NOT EXISTS logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  job_description TEXT,
                  prediction TEXT,
                  confidence REAL,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    # Table: Flagged Posts (Feedback)
    c.execute('''CREATE TABLE IF NOT EXISTS flags
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  job_description TEXT,
                  prediction TEXT,
                  confidence REAL,
                  reason TEXT,
                  status TEXT DEFAULT 'Pending',
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

    # Table: Admin Users (For M4)
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY,
                  password TEXT)''')
             
    # Create default admin if not exists (admin/admin123)
    # real world: hash this. For student project: simple text or basic hash.
    c.execute("INSERT OR IGNORE INTO users VALUES ('admin', 'admin123')")
    
    conn.commit()
    conn.close()
    print("Database initialized.")

def log_prediction(job_text, prediction, confidence):
    """Log every prediction."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO logs (job_description, prediction, confidence) VALUES (?, ?, ?)",
              (job_text, prediction, confidence))
    conn.commit()
    conn.close()

def flag_post(job_text, prediction, confidence, reason):
    """Save a flagged post."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO flags (job_description, prediction, confidence, reason) VALUES (?, ?, ?, ?)",
              (job_text, prediction, confidence, reason))
    conn.commit()
    conn.close()

def get_stats():
    """Get basic stats for dashboard."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM logs")
    total = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM logs WHERE prediction='Fake Job'")
    fake_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM flags")
    flagged_count = c.fetchone()[0]
    
    conn.close()
    return {
        "total_scans": total,
        "fake_detected": fake_count,
        "real_detected": total - fake_count,
        "flagged_by_users": flagged_count
    }

def get_all_flags():
    """Get all flagged posts for the detailed dashboard."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM flags ORDER BY timestamp DESC")
    rows = [dict(row) for row in c.fetchall()]
    conn.close()
    return rows

def verify_user(username, password):
    """Simple check for admin login."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

def update_flag_status(flag_id, status):
    """Update status of a flagged post."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE flags SET status=? WHERE id=?", (status, flag_id))
    conn.commit()
    conn.close()

def delete_flag(flag_id):
    """Delete a flagged post."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM flags WHERE id=?", (flag_id,))
    conn.commit()
    conn.close()

def clear_logs():
    """Clear all prediction logs."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM logs")
    conn.commit()
    conn.close()
