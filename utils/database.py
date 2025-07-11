from pathlib import Path
import sqlite3

current_dir = Path().resolve()

class DataBase:
    def __init__(self) -> None:
        self.db = sqlite3.connect(current_dir / "data.db")
        self.cursor = self.db.cursor()
        cmd = "CREATE TABLE IF NOT EXISTS data (id INT, user_id INT, msg_text TEXT)"
        self.cursor.execute(cmd)
        self.db.commit()


    def save_data(self, id, userid, text) -> None:
        cmd = f"INSERT INTO data VALUES ('{int(id)}','{int(userid)}', '{str(text)}')"
        self.cursor.execute(cmd)
        self.db.commit()


    def update_data(self, userid, text) -> None:
        cmd = f"UPDATE data SET msg_text={text} WHERE user_id={userid}"
        self.cursor.execute(cmd)
        self.db.commit()


    def read_data(self) -> dict:
        cmd = f"SELECT * FROM data"
        self.cursor.execute(cmd)
        data = dict()
        for id, message, data in self.cursor.fetchall():
            # avoiding possible duplication
            if int(id) not in data.keys():
                data[int(id)] = (message, data)
        return data
    

    def get_data(self, id) -> list:
        cmd = f'SELECT * FROM data WHERE id={int(id)}'
        self.cursor.execute(cmd)
        
        return self.cursor.fetchall()


    def exec(self, cmd) -> list:
        self.cursor.execute(cmd)
        return self.cursor.fetchall()
    
    
    def get_id(self) -> int:
        with open('./utils/db_ids.txt', 'r') as f:
            a = f.readline()
            
        return a
    
    def get_new_id(self) -> int:
        a = int(self.get_id()) + 1
        with open('./utils/db_ids.txt', 'w') as f:
            f.write(str(a))
        
        return a
    

database = DataBase()