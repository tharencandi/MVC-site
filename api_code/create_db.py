import sqlite3

con = sqlite3.connect('database.db')
cur = con.cursor()



#Users
cur.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0
        )''')

#Posts
cur.execute('''
        CREATE TABLE IF NOT EXISTS Posts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author_id INTEGER NOT NULL,
            forum TEXT NOT NULL,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            parent_id INTEGER DEFAULT -1,
            FOREIGN KEY (author_id) REFERENCES Users (id)
        )''')




## dummy data

cur.execute("INSERT INTO Users VALUES (0,'username_1','password_1',0)")
cur.execute("INSERT INTO Users VALUES (1,'bob','pword',0)")
cur.execute("INSERT INTO Users VALUES (2,'alice','yep',0)")

cur.execute("INSERT INTO Posts VALUES (0,0,'general','a question about thing','body to question', -1)")

cur.execute("INSERT INTO Posts VALUES (1,1,'general','this is a reply!','hello', 0)")
cur.execute("INSERT INTO Posts VALUES (2,2,'general','this is another reply!','i am alice', 0)")
con.commit()

#for row in cur.execute('SELECT * FROM Posts'):
       # print(row)



con.close()
