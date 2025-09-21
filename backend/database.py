
import sqlite3

DATABASE_PATH = "chattube.db"

class Database:
    def __init__(self):
        self.dbPath = DATABASE_PATH
        self.__init_db__()

    def __init_db__(self):
        """Create database and table if it doesn't exist"""

        conn = sqlite3.connect(self.dbPath)
        cursor = conn.cursor()
        cursor.execute("""
                           CREATE TABLE IF NOT EXISTS chatHistory (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               sessionID TEXT NOT NULL,
                               role TEXT NOT NULL,
                               content TEXT NOT NULL,
                               timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                           )
                       """
        )
        cursor.execute("""
                           CREATE TABLE IF NOT EXISTS videoInfo (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               videoID TEXT NOT NULL,
                               sessionID TEXT NOT NULL,
                               timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                           )
                       """
        )
        cursor.execute(
            """
                CREATE INDEX IF NOT EXISTS idxSessionID
                ON chatHistory (sessionID, timestamp)
            """
        )
        cursor.execute(
            """
                CREATE INDEX IF NOT EXISTS idxVideoID
                ON videoInfo (videoID, timestamp)
            """
        )
        conn.commit()
        conn.close()

    def get_db_path(self):
        return self.dbPath
