
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
    def add_user(self, details):
        #check if username exists
        try:
            self.cur.execute("INSERT INTO Users (username, password, salt, is_admin) VALUES (?,?,?,?)", details)
            self.conn.commit()
            return (True, None)
        except sqlite3.OperationalError:
            return (False, "Internal server error")
        except sqlite3.IntegrityError:
            return (False, "username already exists")
    
    #details (username, hashed_password)
    def check_credentials(self, username, password):
        try:
          
            query = "SELECT u.id, password, salt FROM Users u WHERE u.username=?;"
            result = self.cur.execute(query,(username,)).fetchall()[0]
            #result = self.db_get_request(query, (username))
         
            #print(bcrypt.hashpw(password.encode(),result["salt"]))
            if result["password"] ==  bcrypt.hashpw(password.encode(),result["salt"].encode()).decode():
                return (True, result["id"])
            return (False, None)
        except sqlite3.OperationalError as e:
            print(e)
            return (False, None)


    def delete_user(self, id):
        query = "DELETE FROM Users u WHERE u.id=?;"
        self.cur.execute(query,(id,))
        self.conn.commit()
        return True

    def get_user(self, id ):
        pass

    def admin_data(self):
        query = """Select p.id, report_count, username FROM Posts p JOIN Users u ON p.author_id = u.id;"""
        results = self.cur.execute(query).fetchall()
        return json.dumps(results)

    """ 
        FORUM STUFF 
    """
   
    def get_posts(self, forum):
        query = """SELECT p.id, title, body, author_id, username FROM Posts p JOIN Users u ON p.author_id = u.id WHERE FORUM=?;"""
        try:
            results = self.db_get_request(query, (forum,))
            return json.dumps(results)
        except sqlite3.OperationalError:
            return None

    def get_post(self, id):
        query = "SELECT p.id, forum, title, body, author_id, username FROM Posts p JOIN Users u ON p.author_id = u.id WHERE p.id =? ;"
        results = self.db_get_request(query, (id,))
        return json.dumps(results)

    def delete_post(self, id):
        query = "DELETE FROM Posts p WHERE p.id=?;"
        self.cur.execute(query,(id,))
        self.conn.commit()
        return True
    
    def get_post_thread(self, id):
        query = "SELECT p.id, title, body, author_id, username FROM Posts p JOIN Users u ON p.author_id = u.id WHERE p.id =? OR p.parent_id=?;"
        try:
            results = self.db_get_request(query, (id,id))
            return json.dumps(results)
        except sqlite3.OperationalError:
            return None
    
    def report_post(self, id):
        query = "UPDATE Posts SET report_count=report_count+1 WHERE id=?;"
        self.cur.execute(query, (id,))
        self.conn.commit()

    #post_details :(author_id, forum, title, body, parent_id )
    def add_post(self, post_details):
        print("post details", post_details)
        query = "INSERT INTO Posts (author_id, forum, title, body, parent_id) VALUES (?, ?, ?, ?, ?);"
        try:
            self.cur.execute(query, tuple(post_details))
            self.conn.commit()
            return True
        except sqlite3.OperationalError:
            return False
        


    
