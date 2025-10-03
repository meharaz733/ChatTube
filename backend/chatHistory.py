"""Chat History, store and return user chat message..."""

import sqlite3
from typing import List, Tuple

class ChatHistory:
    def __init__(self, sessionID:str, dbPath):
        self.sessionID = sessionID
        self.dbPath = dbPath

    def __saveMessage__(self, data: List[Tuple[str, str]]):
        """PUSH user chat into the chat history database"""

        conn = sqlite3.connect(self.dbPath)
        cursor = conn.cursor()
        for role, content in data:
            cursor.execute(
                """
                INSERT INTO chatHistory (sessionID, role, content) VALUES (?, ?, ?)
                """,
                    (self.sessionID, role, content)
            )
        conn.commit()
        conn.close()

    def __loadMessage__(self, k):
        """
        Retrieve chat history from the db and return a it as list of tuples.
        """
        
        conn = sqlite3.connect(self.dbPath)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT role, content FROM chatHistory WHERE sessionID = ? ORDER BY timestamp DESC LIMIT ?
            """,
            (self.sessionID, k)
        )
        results = cursor.fetchall()
        conn.close()

        return [(role, content) for role, content in reversed(results)]
