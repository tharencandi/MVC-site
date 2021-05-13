import socket
import sys
import json
#check json formatting
query = {
        "function": "add_user",
        "params": {"username": "nick", "password": "sadasdsads", "salt" :"s", "is_admin":0},
        "auth": "password"
        }

     


HOST, PORT = "localhost", 9999
data = " ".join(sys.argv[1:])

# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto().
data = json.dumps(query)
sock.sendto(bytes(data, encoding="utf-8"), (HOST, PORT))
#sock.sendto(bytes(data + "\n", "utf-8"), (HOST, PORT))
received = str(sock.recv(1024), "utf-8")

print("Sent:     {}".format(data))
print("Received: {}".format(received))