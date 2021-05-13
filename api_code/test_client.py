
import requests
query = {"forum": "general"}
query1 = {"id": 0}

'''
        CREATE TABLE IF NOT EXISTS Posts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author_id INTEGER NOT NULL,
            forum TEXT NOT NULL,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            parent_id INTEGER DEFAULT -1,
            FOREIGN KEY (author_id) REFERENCES Users (id)
        )'''
auth="my super secret token"
new_post =
{"forum": "general", 



}

#print("\n--------------\nGET ALL GENERAL FORUM POSTS\n--------------\n")
r = requests.get('http://127.0.0.1:5001/api/forum',params=query)
#print(r.url)
#print(r.text)
#data = r.json()[0]
#print(data)


#print("\n--------------\nGET POST THREAD id = 0\n--------------\n")

r = requests.get('http://127.0.0.1:5001/api/post_thread',params=query1)
#print(r.url)
#print(r.text)
#data = r.json()
#print(data)

r = requests.post('http://127.0.0.1:5001/api/post')
print(r.text)
