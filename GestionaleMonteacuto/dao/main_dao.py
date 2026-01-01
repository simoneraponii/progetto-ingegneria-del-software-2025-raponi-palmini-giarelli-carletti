import pyodbc
from DB_CONFIG import DB_CONFIG

class MainDAO:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            if self.conn is None:
                conn_str = (
                    f"DRIVER={DB_CONFIG['driver']};"
                    f"SERVER={DB_CONFIG['server']};"
                    f"DATABASE={DB_CONFIG['database']};"
                    f"Trusted_Connection={DB_CONFIG['trusted_connection']};"
                )
                self.conn = pyodbc.connect(conn_str)
                self.cursor = self.conn.cursor()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to database: {e}")

    def disconnect(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        except Exception:
            pass 
        finally:
            self.cursor = None
            self.conn = None
