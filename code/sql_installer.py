import sqlite3
conn = sqlite3.connect('database.db')


conn.execute("""REATE TABLE Posts(
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            author_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            FOREIGN KEY (author_Id) REFERENCES Users (Id)""")

            
