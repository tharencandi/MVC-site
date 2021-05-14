from json.decoder import JSONDecodeError
import socketserver
import json
from database_manager import db_manager

db = db_manager()

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(2048).strip()

        response = db.safe_transaction_wrapper(data)
        
        self.request.sendall(str(response).encode())

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
