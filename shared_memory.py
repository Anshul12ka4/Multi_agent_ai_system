import sqlite3
import json
from datetime import datetime

class SharedMemory:
    def __init__(self, db_path='memory.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                type TEXT,
                intent TEXT,
                timestamp TEXT,
                sender TEXT,
                conversation_id TEXT,
                fields TEXT
            )
        """)

    def log(self, source, type_, intent, sender=None, conversation_id=None, fields="{}"):
        # Convert fields to JSON string if it's a dict
        if isinstance(fields, dict):
            fields = json.dumps(fields)

        self.conn.execute("""
            INSERT INTO memory (source, type, intent, timestamp, sender, conversation_id, fields)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (source, type_, intent, datetime.now().isoformat(), sender, conversation_id, fields))
        self.conn.commit()
