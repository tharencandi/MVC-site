
import requests
query = {"forum": "general"}
query1 = {"id": 0}
query2 = {"id": 0, "is_reply": 1}


print("\n--------------\nGET ALL GENERAL FORUM POSTS\n--------------\n")
r = requests.get('http://127.0.0.1:5001/api/forum',params=query)
print(r.url)
data = r.json()
print(data)


print("\n--------------\nGET POST id = 0\n--------------\n")

r = requests.get('http://127.0.0.1:5001/api/post',params=query1)
print(r.url)
data = r.json()
print(data)

print("\n--------------\nGET POST id = 0 REPLIES\n--------------\n")

r = requests.get('http://127.0.0.1:5001/api/post',params=query2)
print(r.url)
data = r.json()
print(data)