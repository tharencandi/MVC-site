
import sqlite3
import json
import bcrypt

forums=["general", "html", "htww", "javascript", "web-frameworks"]
def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d


class db_manager:
    def __init__(self, ):
            self.conn = sqlite3.connect('database.db')
            self.conn.row_factory = dict_factory
            self.cur = self.conn.cursor()

            #Users
            self.cur.execute('''
                    CREATE TABLE IF NOT EXISTS Users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL,
                        salt TEXT NOT NULL,
                        is_admin INTEGER DEFAULT 0
                    )''')
    
            #Posts
            self.cur.execute('''
                    CREATE TABLE IF NOT EXISTS Posts(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        author_id INTEGER NOT NULL,
                        forum TEXT NOT NULL,
                        title TEXT NOT NULL,
                        body TEXT NOT NULL,
                        parent_id INTEGER DEFAULT -1,
                        report_count INTEGER DEFAULT 0,
                        FOREIGN KEY (author_id) REFERENCES Users (id)
                    )''')

            self.conn.commit()
    
   
    def db_get_request(self, query, to_filter):
        results = self.cur.execute(query, tuple(to_filter)).fetchall()
        #self.conn.close()
        return results


    #details (username, hashed_password, salt)
    def add_user(self, params):
        #check if username exists
        try:
            query = "INSERT INTO Users (username, password, salt, is_admin) VALUES (?,?,?,?)"
            self.cur.execute(query, (params['username'], params['password'], params['salt'], params['is_admin']))
            self.conn.commit()
            ret = {"success": True}
            return json.dumps(ret)
        except sqlite3.OperationalError:
            ret = {"success": False, "error_msg": "Internal server error"}
            return json.dumps(ret)
        except sqlite3.IntegrityError:
            ret = {"success": False, "error_msg": "username already exists"}
            return json.dumps(ret)
    
    #details (username, hashed_password)
    def check_credentials(self, params):
        try:
            query = "SELECT u.id, password, salt FROM Users u WHERE u.username=?;"
            result = self.cur.execute(query,(params["username"],)).fetchall()
            if len(result) != 0:
                result = result[0]
                if result["password"] == params["password"]:
                    print("SUCCCCCC")
                    return json.dumps({"success": True, "id": result["id"]})
            return json.dumps({"success": False})
        except sqlite3.OperationalError as e:
            print(e)
            return json.dumps({"success": False})


    def delete_user(self, params):
        query = "DELETE FROM Users u WHERE u.id=?;"
        self.cur.execute(query,(params["id"],))
        self.conn.commit()
        return json.dumps({"success": True})

    #def get_user(self, params ):
     #   pass

    def get_salt_by_username(self, params):
        query = """SELECT p.salt FROM Users p WHERE p.username =?;"""
        results = self.cur.execute(query, (params["username"], )).fetchall()
        return json.dumps(results)


    def admin_data(self):
        query = """Select p.id, report_count, username FROM Posts p JOIN Users u ON p.author_id = u.id;"""
        results = self.cur.execute(query).fetchall()
        return json.dumps(results)

    """ 
        FORUM STUFF 
    """
   
    def get_posts(self, params):
        query = """SELECT p.id, title, body, author_id, username FROM Posts p JOIN Users u ON p.author_id = u.id WHERE FORUM=? AND p.parent_id= -1;"""
        try:
            results = self.db_get_request(query, (params["forum"],))
            return json.dumps(results)
        except sqlite3.OperationalError:
            return None

    def get_post(self, params):
        query = "SELECT p.id, forum, title, body, author_id, username FROM Posts p JOIN Users u ON p.author_id = u.id WHERE p.id =? ;"
        results = self.db_get_request(query, (params["id"],))
        return json.dumps(results)

    def delete_post(self, params):
        query = "DELETE FROM Posts p WHERE p.id=?;"
        self.cur.execute(query,(params["id"],))
        self.conn.commit()
        return json.dumps({"success": True})
    
    def get_post_thread(self, params):
        query = "SELECT p.id, title, body, author_id, username FROM Posts p JOIN Users u ON p.author_id = u.id WHERE p.id =? OR p.parent_id=?;"
        try:
            results = self.db_get_request(query, (params["id"],params["id"]))
            return json.dumps(results)
        except sqlite3.OperationalError:
            return None
    
    def report_post(self, params):
        query = "UPDATE Posts SET report_count=report_count+1 WHERE id=?;"
        self.cur.execute(query, (params["id"],))
        self.conn.commit()
        return json.dumps({"success": True})

    #post_details :(author_id, forum, title, body, parent_id )
    def add_post(self, params):
        print("post details", params)
        query = "INSERT INTO Posts (author_id, forum, title, body, parent_id) VALUES (?, ?, ?, ?, ?);"
        try:
            self.cur.execute(query, (params["author_id"],params["forum"], params["title"], params["body"], params["parent_id"]))
            self.conn.commit()
            return json.dumps({"success": True})
        except sqlite3.OperationalError:
            return json.dumps({"success": False})
        


    
