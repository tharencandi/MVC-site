import sqlite3

# This class is a simple handler for all of our SQL database actions
# Practicing a good separation of concerns, we should only ever call 
# These functions from our models

# If you notice anything out of place here, consider it to your advantage and don't spoil the surprise

class SQLDatabase():
    '''
        Our SQL Database

    '''

    # Get the database running
    def __init__(self, database_arg=":memory:"):
        self.conn = sqlite3.connect(database_arg)
        self.cur = self.conn.cursor()

    # SQLite 3 does not natively support multiple commands in a single statement
    # Using this handler restores this functionality
    # This only returns the output of the last command
    def execute(self, sql_string):
        out = None
        for string in sql_string.split(";"):
            try:
                out = self.cur.execute(string)
            except:
                pass
        return out

    # Commit changes to the database
    def commit(self):
        self.conn.commit()

    #-----------------------------------------------------------------------------
    
    # Sets up the database
    # Default admin password
    def database_setup(self, admin_password='admin'):


        # Create the users table
        self.execute("""
        CREATE TABLE IF NOT EXISTS Users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            admin INTEGER DEFAULT 0
        )""")

        self.commit()

        self.execute("""
        CREATE TABLE IF NOT EXISTS Posts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author_id INTEGER NOT NULL,
            forum TEXT NOT NULL,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            parent_id INTEGER DEFAULT -1,
            FOREIGN KEY (author_id) REFERENCES Users (id)
        """)

        # Add our admin user
        self.add_user('admin', admin_password, is_admin=True)

    #-----------------------------------------------------------------------------
    # User handling
    #-----------------------------------------------------------------------------

    def get_next_user_id(self):
        '''Return the current max id + 1 in the database for new user creation'''
        sql_cmd = "SELECT MAX(id) FROM Users"
        max_id = self.execute(sql_cmd)
        if max_id == None:
            # Database has not been initialised
            return 0
        else:
            max_id = max_id.fetchone()[0]
            if max_id == None:
                # No id in database
                return 0
        return max_id + 1

    def check_user_exist(self, username):
        '''Check if a username exist in database.'''
        sql_cmd = f"SELECT username FROM Users WHERE username = '{username}'"
        
        cursor = self.execute(sql_cmd)

        if cursor == None:
            return False
        result = cursor.fetchone()

        if result == None:
            return False
        elif result[0] != username:
            return False
        return True

    def check_id_exist(self, id):
        '''Check if a username exist in database.'''
        sql_cmd = f"SELECT id FROM Users WHERE id = {id}"
        
        cursor = self.execute(sql_cmd)

        if cursor == None:
            return False
        result = cursor.fetchone()
        if result == None:
            return False
        elif result[0] != id:
            return False
        return True

    # Add a user to the database
    def add_user(self, username, password, is_admin=False):
        sql_cmd = """
                INSERT INTO Users
                VALUES({id}, '{username}', '{password}', {admin})
            """

        msg = None
        new_id = self.get_next_user_id()

        if is_admin == True:
            admin = 1
        else:
            admin = 0

        if self.check_user_exist(username):
            return (False, "User creation failed: Username exists.")
        elif self.check_id_exist(new_id):
            return (False, "User creation failed: ID exists.")

        sql_cmd = sql_cmd.format(id=new_id, username=username, password=password, admin=admin)

        self.execute(sql_cmd)
        self.commit()
        return (True, msg)

    #-----------------------------------------------------------------------------

    # Check login credentials
    def check_credentials(self, username, password):
        sql_query = """
                SELECT 1
                FROM Users
                WHERE username = '{username}' AND password = '{password}'
            """
        sql_query = sql_query.format(username=username, password=password)

        result = self.execute(sql_query)
        # If our query returns
        if result == None:
            return False
        if result.fetchone() != None:
            return True
        else:
            return False

    def dump(self):
        '''Dump database into sql command'''
        with open('dump.sql', 'w') as f:
            for line in self.conn.iterdump():
                f.write('%s\n' % line)