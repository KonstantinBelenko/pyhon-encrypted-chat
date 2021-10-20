import tcp, threading, argparse

# Arguments
ap = argparse.ArgumentParser(description="Server run options")
ap.add_argument("-a", "--ip-address",   required=False, help="Ip address of the server",           type=str,    default='127.0.0.1')
ap.add_argument("-p", "--port",         required=False, help="Port address of the server",         type=int,    default=5000)
ap.add_argument("-q", "--max-querry",   required=False, help="Number of maximum connection queue", type=int,    default=5)
ap.add_argument("-b", "--buffer-size",  required=False, help="Default server buffer size",         type=int,    default=1024)
ap.add_argument("-e", "--encoding",     required=False, help="Default encoding",                   type=str,    default='utf-8')

ap.add_argument("-v", "--verbose",      required=False, help="Verbose on / off",        action='store_true')
ap.add_argument("-c", "--encryption",   required=False, help="Use encryption or not",   action='store_true')

args = vars(ap.parse_args())


# Broadcasting funciton that will be instantiated for each connection
def send_all(client_id):
    while True:
        message     =   server.recv(client_id)
        client_name =   server.get_client_ip(client_id)
        broadcast = f'{client_name}: {message}'

        print(broadcast)

        server.send_all(
            message          = broadcast, 
            ignore_client_id = client_id
        )


if __name__ == "__main__":

    server = tcp.Server(
        args['ip_address'], 
        args['port'], 
        args['buffer_size'], 
        encoding=args['encoding'],
        verbose=args['verbose'],
        encryption=args['encryption']
    )

    server.listen(
        args['max_querry'], 
    )

    while True:
        client_id = server.accept()
        client_name = server.get_client_ip(client_id)

        print(f"Client: {client_name} has connected")

        # Create new therad for each client to broadcast messages across all connections
        thread = threading.Thread(target=send_all, args=(client_id,)).start()

