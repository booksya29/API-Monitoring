from database_sys.database import DataBase
from schemes import ApiScheme

if __name__ == "__main__":
    db = DataBase()
    db.connect()
    db.create_tables()
    db.apidb_controller.add_new_api(ApiScheme(
    creator_id=1,
    url="https://example.com/api/users",
    send_method="GET",
    body='{"user_id": 1}'
))