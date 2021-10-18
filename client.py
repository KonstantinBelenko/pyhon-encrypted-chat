import tcp
import threading

def recv_msg():
    while True:
        print(client.recv())

client = tcp.Client("127.0.0.1", 5000, 1024, encoding="utf-8")
client.connect()

# Start separate receiving thread to not interfere with own messages
recv_thread = threading.Thread(target=recv_msg)
recv_thread.start()

while True:
    client.send(input("> "))