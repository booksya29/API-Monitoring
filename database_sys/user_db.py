from schemes.userdb_schemes import User

class UserDB:
    def __init__(self, conn):
        self.conn = conn

    def check_user(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT EXISTS(SELECT 1 FROM users WHERE id = %s)", (user_id,))
        exists = cursor.fetchone()[0]
        cursor.close()
        return exists
    def add_new_user(self, data:User):
        data_dict = data.model_dump(exclude="register_date")
        if None in data_dict.values():
            return (False, "No required data of user")
        cursor = self.conn.cursor()
        columns = ", ".join(data_dict.keys())
        values = ', '.join(["%s"]*len(data_dict))
        query = f"INSERT INTO users ({columns}) VALUES ({values})"
        cursor.execute(query, tuple(data_dict.values()))
        self.conn.commit()
        cursor.close()
    def test(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT register_date FROM users")
        print(int(cursor.fetchone()[0].timestamp()))

    def change_notification_state(self, user_id, notification_b):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE users SET notification_b = %s WHERE id = %s", (notification_b, user_id))
        self.conn.commit()
        cursor.close()

    def get_notification_state(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT notification_b FROM users WHERE id = %s", (user_id,))
        return cursor.fetchone()[0]
    