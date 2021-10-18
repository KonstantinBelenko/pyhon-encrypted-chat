import tcp
import threading

def send_all(client_id):
    while True:
        msg = server.recv(client_id)
        print(f'{client_id}: {msg}')

        client_name = server.get_client_ip(client_id)
        server.send_all(f'{client_name}: {msg}', ignore_client=client_id)

server = tcp.Server("127.0.0.1", 5000, 1024, encoding='utf-8')
server.listen(2)


while True:
    client_id = server.accept()
    thread = threading.Thread(target=send_all, args=(client_id,)).start()

