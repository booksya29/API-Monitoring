from schemes.historydb_schemes import HistoryScheme
from pandas import DataFrame
class HistoryDB:
    def __init__(self, conn):
        self.conn = conn
    def add_data_to_history(self, data:HistoryScheme):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO history (api_id, status_code, body, user_id) VALUES (%s, %s, %s, %s)",
            (data.api_id, data.status_code, data.body, data.user_id)
        )
        self.conn.commit()

    def get_history_by_user(self, user_id:int):
        cursor = self.conn.cursor()
        cursor.execute("SELECT h.api_id, h.status_code, h.check_time FROM history AS h WHERE h.user_id = %s", (user_id,))
        rows = cursor.fetchall()
        df = DataFrame(rows, columns=["api_id", "status_code", "check_time"])
        return df