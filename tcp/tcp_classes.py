import socket as s
from .tcp_methods import header_the_message, recv

class Server:
    '''
    Server class to simplify socket communication.

    Attributes
    ----------
    IP : str
        The ip adress of the server
    PORT : int
        The port of the server
    BUFFER_SIZE : int
        Default buffer size that the server will use when i/o requests (default is 1024)
    HEADER_SIZE : int
        Default size of a header message containing information that will come before any message is sent (default is 50)
    encoding : str
        Charset that all the messages will be encoded in (default is utf-8)

    '''

    def __init__(self, IP, PORT, BUFFER_SIZE=1024, HEADER_SIZE=50, encoding='utf-8'):
        '''
        Parameters
        ----------
        IP : str
            The ip adress of the server
        PORT : int
            The port of the server
        BUFFER_SIZE : int
            Default buffer size that the server will use when i/o requests (default is 1024)
        HEADER_SIZE : int
            Default size of a header message containing information that will come before any message is sent (default is 50)
        encoding : str
            Charset that all the messages will be encoded in (default is utf-8)
        '''

        self.BUFFER_SIZE = BUFFER_SIZE
        self.IP = IP
        self.PORT = PORT
        self.HEADER_SIZE = HEADER_SIZE
        self.encoding = encoding
    
        self.clients = {}
        self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)

    def listen(self, num_clients:int):
        '''Binds the server and starts listenting for the specified number of clients.
        
        Parameters
        ----------
        num_clients : int
            The number of clients to listen for.
        '''
        self.socket.bind((self.IP, self.PORT))
        self.socket.listen(num_clients)

    def accept(self) -> int:
        '''Returns an ID of an accepted client.'''
        sock, addr = self.socket.accept()

        client_id = len(self.clients) + 1
        self.clients[client_id] = sock

        return client_id

    def get_clients(self, print_clients:bool = False) -> dict:
        '''Returns a dictionary of all clients that've connected to the server
        
        If the argument `print_clients` is passed in, clients dict is printed out.

        Parameters
        ----------
        print_clients : bool
            print clients to the terminal window (default is False)

        '''
        if print_clients:
            print(self.clients)
        return self.clients

    def get_client_ip(self, client_id):
        '''Returns a client ip address by his id in the `clients` dictionary

        Parameters
        ----------
        client_id : int
            Client id in the dictionary

        '''
        return self.clients[client_id].getpeername()[0]

    def send(self, message:str, client_id:int):
        '''Sends a message to a client by the specified client ID.
        
        Parameters
        ----------
        message : str
            Message that will be sent to the client
        client_id : int
            Client id in the dictionary
        '''
        self.clients[client_id].send(
            header_the_message(message, self.HEADER_SIZE)
            .encode(self.encoding)
            )

    def send_all(self, message:str, ignore_client:int = None):
        '''Sends specified message to all clients.

        If the argument `ignore_client` is passed in, specified client will be ignored when sending the message.

        Parameters
        ----------
        message : str
            Message that will be sent to all clients
        ignore_client : int
            Client that will be ignored when sending the message
        '''

        if ignore_client:
            for client in [self.clients[i] for i in self.clients]:
                if client != self.clients[ignore_client]:
                    message = header_the_message(message, self.HEADER_SIZE)
                    client.send(message.encode(self.encoding))
        else:
            for client in [self.clients[i] for i in self.clients]:
                message = header_the_message(message, self.HEADER_SIZE)
                client.send(message.encode(self.encoding))

    def recv(self, client_id:int) -> str:
        '''Returns message received from the client
        
        Parameters
        ----------
        client_id : str
            Client id in the dictionary
        '''
        return recv(self.clients[client_id], self.HEADER_SIZE, self.BUFFER_SIZE)

    def close(self):   
        '''Closes server socket'''
        self.socket.close()



class Client:
    '''
    Client class to simplify socket communication.

    Attributes
    ----------
    IP : str
        The ip adress of the server
    PORT : int
        The port of the server
    BUFFER_SIZE : int
        Default buffer size that the server will use when i/o requests (default is 1024)
    HEADER_SIZE : int
        Default size of a header message containing information that will come before any message is sent (default is 50)
    encoding : str
        Charset that all the messages will be encoded in (default is utf-8)

    '''

    def __init__(self, IP, PORT, BUFFER_SIZE=1024, HEADER_SIZE=50, encoding='utf-8'):
        '''
        Parameters
        ----------
        IP : str
            The ip adress of the server
        PORT : int
            The port of the server
        BUFFER_SIZE : int
            Default buffer size that the server will use when i/o requests (default is 1024)
        HEADER_SIZE : int
            Default size of a header message containing information that will come before any message is sent (default is 50)
        encoding : str
            Charset that all the messages will be encoded in (default is utf-8)
        '''
        self.IP = IP
        self.PORT = PORT
        self.BUFFER_SIZE = BUFFER_SIZE
        self.HEADER_SIZE = HEADER_SIZE
        self.encoding = encoding
    
        self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)

    def connect(self):
        '''Connects to the specified earlier IP and PORT'''
        self.socket.connect((self.IP, self.PORT))

    def send(self, message:str):
        ''' Sends the specified message to the server.
        Parameters
        ----------
        message : str
            Message that will be sent to the server
        '''
        self.socket.send( 
            header_the_message(message, self.HEADER_SIZE).encode(self.encoding)
            )

    def close(self):
        '''Closes the client socket'''
        self.socket.close()

    def recv(self) -> str:
        '''Receives full message'''
        return recv(self.socket, self.HEADER_SIZE, self.BUFFER_SIZE)