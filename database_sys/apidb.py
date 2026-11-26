from schemes import ApiScheme
from psycopg2.extras import RealDictCursor

class ApiDB:
    def __init__(self, conn):
        self.conn = conn
    def add_new_api(self, data:ApiScheme):
        cursor = self.conn.cursor()
        cursor.execute("SELECT EXISTS(SELECT 1 FROM api WHERE creator_id = %s AND url = %s AND send_method = %s AND body = %s)", (data.creator_id, data.url, data.send_method, data.body))
        exists = cursor.fetchone()[0]
        if exists:
            cursor.close()
            return False
        cursor.execute("INSERT INTO api(creator_id, status, url, send_method, body) VALUES(%s,%s,%s,%s,%s)", (data.creator_id, data.status, data.url, data.send_method, data.body))
        self.conn.commit()
        cursor.close()
        return data.model_dump()

    def get_users_api(self, user_id:int):
        cursor = self.conn.cursor(cursor_factory = RealDictCursor)
        cursor.execute("SELECT * FROM api WHERE id = user_id")
        data = cursor.fetchall()
        cursor.close()
        return data

    def change_api_info(self, data:ApiScheme, id:int):
        cursor = self.conn.cursor(cursor_factory = RealDictCursor)
        new_data = data.model_dump()
        sets = ", ".join(f"{key} = %s" for key in new_data.keys())
        query = f"UPDATE api SET {sets} WHERE id = %s"
        cursor.execute(query, tuple(new_data.values(), id))
        self.conn.comit()
        cursor.close()
        