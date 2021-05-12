from json.decoder import JSONDecodeError
import socketserver
import json
from database_manager import db_manager

db = db_manager()

class MyUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]

        response = db.safe_transaction_wrapper(data)
        
        socket.sendto(str(response).encode(), self.client_address)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever()
