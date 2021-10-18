import tcp, threading, argparse

# Arguments
ap = argparse.ArgumentParser(description="Server run options")
ap.add_argument("-a", "--ip-address",   required=False, help="ip address of the server",           type=str, default='127.0.0.1')
ap.add_argument("-p", "--port",         required=False, help="port address of the server",         type=int, default=5000)
ap.add_argument("-q", "--max-querry",   required=False, help="number of maximum connection queue", type=int, default=5)
ap.add_argument("-b", "--buffer-size",  required=False, help="Default server buffer size",         type=int, default=1024)
ap.add_argument("-e", "--encoding",     required=False, help="Default encoding",                   type=str, default='utf-8')
ap.add_argument("-v", "--verbose",      required=False, help="Verbose on / off",                   type=bool, default=False)
args = vars(ap.parse_args())

def send_all(client_id):
    while True:
        msg = server.recv(client_id)
        client_name = server.get_client_ip(client_id)

        print(f'{client_name}: {msg}')

        server.send_all(f'{client_name}: {msg}', ignore_client=client_id)

if __name__ == "__main__":

    server = tcp.Server(args['ip_address'], args['port'], args['buffer_size'], encoding=args['encoding'])
    server.listen(args['max_querry'], verbose=args['verbose'])

    while True:
        client_id = server.accept()
        print(f"Client: {server.get_client_ip(client_id)} has connected")
        thread = threading.Thread(target=send_all, args=(client_id,)).start()

