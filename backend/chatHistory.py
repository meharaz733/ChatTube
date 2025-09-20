"""Chat History, store and return user chat message..."""

import sqlite3
from typing import List, Tuple

class ChatHistory:
    def __init__(self, sessionID:str):
        self.sessionID = sessionID
        self.dbPath = "chatHistory.db"
        self.__init_db__()

    def __init_db__(self):
        """Create database and table if it doesn't exist"""

        conn = sqlite3.connect(self.dbPath)
        cursor = conn.cursor()
        cursor.execute("""
                           CREATE TABLE IF NOT EXISTS messages (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               sessionID TEXT NOT NULL,
                               role TEXT NOT NULL,
                               content TEXT NOT NULL,
                               timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                           )
                       """
        )
        cursor.execute(
            """
                CREATE INDEX IF NOT EXISTS idxSessionID
                ON messages (sessionID, timestamp)
            """
        )
        conn.commit()
        conn.close()
        
        

    def __saveMessage__(self, data: List[Tuple[str, str]]):
        """PUSH user chat into the chat history database"""

        conn = sqlite3.connect(self.dbPath)
        cursor = conn.cursor()
        for role, content in data:
            cursor.execute(
                """
                INSERT INTO messages (sessionID, role, content) VALUES (?, ?, ?)
                """,
                    (self.sessionID, role, content)
            )
        conn.commit()
        conn.close()

    def __loadMessage__(self, k):
        """
        Retrieve chat history from the db and return a it as list of dictionaries.
        """
        
        conn = sqlite3.connect(self.dbPath)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT role, content FROM messages WHERE sessionID = ? ORDER BY timestamp DESC LIMIT ?
            """,
            (self.sessionID, k)
        )
        results = cursor.fetchall()
        conn.close()

        return [(role, content) for role, content in reversed(results)]
