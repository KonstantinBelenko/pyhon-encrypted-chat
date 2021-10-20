import tcp, threading, argparse

# Arguments
ap = argparse.ArgumentParser(description="Server run options")
ap.add_argument("-a", "--ip-address",   required=False, help="Ip to connect to",            type=str,  default='127.0.0.1')
ap.add_argument("-p", "--port",         required=False, help="Port to connect to",          type=int,  default=5000)
ap.add_argument("-b", "--buffer-size",  required=False, help="Default client buffer size",  type=int,  default=1024)

ap.add_argument("-v", "--verbose",      required=False, help="Verbose on / off",        action='store_true')
ap.add_argument("-e", "--encryption",   required=False, help="Use encryption or not",   action='store_true')
args = vars(ap.parse_args())

# Separate thread for reading messages.
def recv_msg():
    while True:
        print(client.recv())

client = tcp.Client(
    args['ip_address'], 
    args['port'], 
    args['buffer_size'], 
    verbose=args['verbose'],
    encryption=args['encryption']
)

client.connect()

# Start separate receiving thread to not interfere with own messages
recv_thread = threading.Thread(target=recv_msg)
recv_thread.start()

while True:
    client.send(input("> "))