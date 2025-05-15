#app_server.py

from xmlrpc.server import SimpleXMLRPCServer

#Data from .db
data = {
    "try": "Congrats!"
}

def get_data(user_id):
    return data.get(user_id, "Try again :(")

server = SimpleXMLRPCServer(("localhost", 8000))
print("RPC server running on port 8000...")

server.register_function(get_data, "get_data")
server.serve_forever()