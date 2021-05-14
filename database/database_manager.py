
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
    def __init__(self):
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
                        is_admin INTEGER DEFAULT 0,
                        is_banned INTEGER DEFAULT 0
                    )''')
    
            #Posts
            self.cur.execute('''
                    CREATE TABLE IF NOT EXISTS Posts(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        author_id INTEGER NOT NULL,
                        forum TEXT NOT NULL,
                        title TEXT,
                        body TEXT NOT NULL,
                        parent_id INTEGER DEFAULT -1,
                        report_count INTEGER DEFAULT 0,
                        FOREIGN KEY (author_id) REFERENCES Users (id)
                    )''')
            
            self.conn.commit()

            self.actions = {
  
                "add_user": self.add_user,
                "check_credentials": self.check_credentials,
                "delete_user": self.delete_user,
                "admin_data": self.admin_data,
                "get_posts": self.get_posts,
                "get_post": self.get_post, 
                "delete_post": self.delete_post,
                "get_post_thread": self.get_post_thread,
                "report_post": self.report_post,
                "add_post": self.add_post,
                "get_salt_by_username": self.get_salt_by_username,
                "is_admin": self.is_admin
            }
        
            admins = [
                {"username": "haeata", "password": "$2b$12$8jinT1wqx3znObyTsNH1fePlXwGNljj.WjvxmPPHZnwHMHKHqn9ma", "salt": "$2b$12$8jinT1wqx3znObyTsNH1fe", "is_admin": 1},
                {"username": "mariam", "password": '$2b$12$TbwX8/Iu1QzvVU1n6wo5LelLYhiClW5cDep.Lu/5uP18cHb41Qgv.', "salt": '$2b$12$TbwX8/Iu1QzvVU1n6wo5Le', "is_admin": 1},
                {"username": "roy", "password": '$2b$12$Jg0Q53aVRzdAj4RfVcC8LOGpvafwku1zAmhQ2IaxQ1Afc9lqc54ly', "salt": '$2b$12$Jg0Q53aVRzdAj4RfVcC8LO', "is_admin": 1},
                {"username": "candiman", "password": '$2b$12$JRl3w.15i0Ung0EKR9kYBO01lPkg0i64cnySB7wHDbBlfhB5hfezu', "salt": '$2b$12$JRl3w.15i0Ung0EKR9kYBO', "is_admin": 1}
            ]
            for admin in admins:
                self.add_user(admin)
    
    """Safe transaction. Logging should be done here"""
    def safe_transaction_wrapper(self, data):
        response = None
        if not data:
            response = self.error_response("No data provided.", None)
        
        try:
            data = data.decode()
            data = json.loads(data)
        except ValueError:
                response = self.error_response("Couldn\'t decode data.")
                return self.response_builder(response)

        try:
            params = data["params"]
        except ValueError:
            response = self.error_response("No params field.")
            return self.response_builder(response)

        try:
            function = data["function"]
        except KeyError:
            response = self.error_response("No function field.")
            return self.response_builder(response)

        try:
            callback = self.actions[function]
        except KeyError:
            response = self.error_response("No function field.")
            return self.response_builder(response)

        
        # run function
        try:
            response = callback(params)
        except sqlite3.OperationalError as e:
            print("here")
            print(e)
            response = self.error_response("Database operational error.", params)
        except KeyError:
            response = self.error_response("Missing or bad parameter.", params)

        return self.response_builder(response)

    
    """Error has response, error logging should be done here"""
    def error_response(self, message, req_params=None):
        if message:
            response = {"status": False, "message": message}
        else:
            response = {"status": False, "message": "Bad request."}

        return response
    

    """
    Safe response builder. Will return error response if it fails.
    """
    def response_builder(self, response):
        if not response:
            response = self.error_response(None)

        try:
            json_res = json.dumps(response)
        except ValueError:
            json_res = json.dumps(self.error_response("Bad response format."))

        return json_res
    
   
    def db_get_request(self, query, to_filter):
        results = self.cur.execute(query, tuple(to_filter)).fetchall()
        #self.conn.close()
        return results


    #details (username, hashed_password, salt)
    def add_user(self, params):
        #check if username exists
        response = None
        try:
            query = "INSERT INTO Users (username, password, salt, is_admin, is_banned) VALUES (?,?,?,?,0)"
            print("here")
            print(params['password'])
            self.cur.execute(query, (params['username'], params['password'], params['salt'], params['is_admin']))

            self.conn.commit()
            uid = self.get_user_id({"username": params["username"]})
            response = {"status": True, "id": uid, "message": None}

        except sqlite3.IntegrityError:
            response = {"status": False, "message": "Username already exists"}

        return response

    
    #details (username, hashed_password)
    def check_credentials(self, params):
        print("checking creds")
        print(self.cur.execute("SELECT * FROM Users").fetchall())
        query = "SELECT u.id, password, salt, is_admin FROM Users u WHERE u.username=?;"
        print("here")
        print(params)
        result = self.cur.execute(query,(params["username"],)).fetchall()
        print(result)

        if result:
         
            result = result[0]
            if result["password"] == params["password"]:
                return {"status": True, "id": result["id"], "is_admin": result["is_admin"]}
            else:
                return {"status": False, "message": "Passwords do not match"}
        
        print(" correct")
        return {"status": False, "message": "Username does not match"}


    def delete_user(self, params):
        query = "DELETE FROM Users u WHERE u.id=?;"
        self.cur.execute(query,(params["id"],))
        self.conn.commit()
        return {"status": True}

    def ban_user(self, params):
        query = "UPDATE Users SET is_banned=1 WHERE id=?;"
        self.cur.execute(query, (params["id"],))
        self.conn.commit()
        return {"status": True}

    def unban_user(self, params):
        query = "UPDATE Users SET is_banned=0 WHERE id=?;"
        self.cur.execute(query, (params["id"],))
        self.conn.commit()
        return {"status": True}
    
    def is_banned(self, params):
        query = """SELECT is_banned FROM Users u WHERE id =?;"""
        results = self.cur.execute(query, (params["id"], )).fetchall()
        return {"status": True, "is_banned": results}

    def get_user_id(self, params):
        query = """SELECT u.id FROM Users u WHERE u.username=?;"""
        res = self.cur.execute(query, (params["username"], )).fetchone()
        print("asdasdasdasdasdasdasd: ")
        print(res)
        return res

    def get_salt_by_username(self, params):
        query = """SELECT p.salt FROM Users p WHERE p.username =?;"""
        print(params)
        results = self.cur.execute(query, (params["username"], )).fetchall()
        print(results)
        if not results:
            return {"status": False, "data": results}

        else:
            return {"status": True, "data": results}


    def admin_data(self):
        query = """Select p.id, report_count, username FROM Posts p JOIN Users u ON p.author_id = u.id;"""
        results = self.cur.execute(query).fetchall()
        return {"status": True, "data": results}

    """ 
        FORUM STUFF 
    """
   
    def get_posts(self, params):
        query = """SELECT p.id, title, body, forum, author_id, username FROM Posts p JOIN Users u ON p.author_id = u.id WHERE FORUM=? AND p.parent_id= -1;"""
        results = self.db_get_request(query, (params["forum"],))
        return {"status": True, "data": results}

    def get_post(self, params):
        query = "SELECT p.id, forum, title, body, author_id, username FROM Posts p JOIN Users u ON p.author_id = u.id WHERE p.id =? ;"
        results = self.db_get_request(query, (params["id"],))
        return {"status": True, "data": results}

    def delete_post(self, params):
        query = "DELETE FROM Posts p WHERE p.id=?;"
        self.cur.execute(query,(params["id"],))
        self.conn.commit()
        return {"status": True}
    
    def get_post_thread(self, params):
        query = "SELECT p.id, title, body, author_id, username FROM Posts p JOIN Users u ON p.author_id = u.id WHERE p.id =? OR p.parent_id=?;"
        results = self.db_get_request(query, (params["id"],params["id"]))
        return {"status": True, "data": results}
    
    def report_post(self, params):
        query = "UPDATE Posts SET report_count=report_count+1 WHERE id=?;"
        self.cur.execute(query, (params["id"],))
        self.conn.commit()
        return {"status": True}

    #post_details :(author_id, forum, title, body, parent_id )
    def add_post(self, params):
        query = "INSERT INTO Posts (author_id, forum, title, body, parent_id) VALUES (?, ?, ?, ?, ?);"
        self.cur.execute(query, (params["author_id"],params["forum"], params["title"], params["body"], params["parent_id"]))
        self.conn.commit()
        return {"status": True}
    
    def is_admin(self, params):
        print("params")
        query = """SELECT u.is_admin FROM Users u WHERE u.id=?;"""
        results = self.db_get_request(query, (params['user_id']))
        return {"status": True, "data": results}


    
