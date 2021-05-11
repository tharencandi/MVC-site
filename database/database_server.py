from json.decoder import JSONDecodeError
import socketserver
import json
from database_manager import db_manager

db = db_manager()

db_functions = {
    "add_user": db.add_user,
    "check_credentials": db.check_credentials,
    "delete_user": db.delete_user,
    "get_user": db.get_user,
    "admin_data": db.admin_data,
    "get_posts": db.get_posts,
    "get_post": db.get_post, 
    "delete_post": db.delete_post,
    "get_post_thread": db.get_post_thread,
    "report_post": db.report_post,
    "add_post": db.add_post,
    "get_salt_by_username": db.get_salt_by_username,
    "is_admin": db.is_admin
}

def parse_request(data):
    try:
        request = json.loads(data.decode())
        print(request)
        if "function" not in request:
            return None
        if request["function"] not in db_functions:
            return None

        return request
    except JSONDecodeError:
        return None

class MyUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        
        req = parse_request(data)
        ret = db_functions[req["function"]](req["params"])
        socket.sendto(str(ret).encode(), self.client_address)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever()
