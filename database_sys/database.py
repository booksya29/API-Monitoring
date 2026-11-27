import psycopg2
from os import getenv
from dotenv import load_dotenv
from database_sys.apidb import ApiDB
from database_sys.user_db import UserDB
from database_sys.history_db import HistoryDB
from pathlib import Path
env_path = Path(__file__).parent.parent.absolute() / ".env"

load_dotenv(env_path)


class DataBase:
    def __init__(self):
        self.conn = None
        self.apidb_controller = None
        self.usersdb_controller = None
        self.historydb_controller = None
    def connect(self):
        self.conn = psycopg2.connect(
            dbname = getenv("DB_NAME"),
            host = getenv("DB_HOST"),
            port = getenv("DB_PORT"),
            password = getenv("DB_PASSWORD"), 
            user = getenv("DB_USER")
        )
        self.apidb_controller = ApiDB(self.conn) 
        self.usersdb_controller = UserDB(self.conn)
        self.historydb_controller = HistoryDB(self.conn)
        return self.conn


    def create_tables(self):
        if self.conn is None:
            return False
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS api(id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY, creator_id BIGINT, status BOOLEAN, url TEXT, send_method TEXT CHECK(send_method IN ('GET', 'POST', 'PUT', 'DELETE', 'PATCH')), body TEXT, created_at TIMESTAMPTZ DEFAULT NOW(), last_check_seconds TIMESTAMPTZ, max_delay_seconds BIGINT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS users(id BIGINT PRIMARY KEY, name TEXT, api_count INTEGER, register_date TIMESTAMPTZ DEFAULT NOW())")
        cursor.execute("CREATE TABLE IF NOT EXISTS history(id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY , api_id INTEGER NOT NULL, status_code INTEGER NOT NULL, body TEXT NOT NULL, check_time TIMESTAMPTZ DEFAULT NOW(), user_id BIGINT)")
        self.conn.commit()
    def disconect(self):
        self.conn.close()
        self.conn = None
        return True

