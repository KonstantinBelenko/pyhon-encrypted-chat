import socket as s
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from .tcp_methods import header_the_message, recv, split_message

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
    verbose : bool
        Displays server information (default is False)
    encryption : bool
        Sets the encryption level to twice the buffer size, 0 if False (default is True)

    '''

    def __init__(self, IP:str, PORT:int, BUFFER_SIZE: int=1024, HEADER_SIZE: int=50, encoding: str='utf-8', verbose: bool=False, encryption: bool=True) -> None:
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
        verbose : bool
            Displays server information (default is False)
        encryption : bool
            Sets the encryption level to twice the buffer size, 0 if False (default is True)
        '''

        self.BUFFER_SIZE = BUFFER_SIZE
        self.IP = IP
        self.PORT = PORT
        self.HEADER_SIZE = HEADER_SIZE
        self.encoding = encoding
        self.verbose = verbose

        if encryption:
            self.encryption = BUFFER_SIZE * 2
        else:
            self.encryption = 0
    
        # The Dictionary is set in the format:
        # [client_socket]                               if the encryption == 0
        # [client_socket, encrypt_key, decrypt_key]     if the encryption  > 0
        self.clients = {}
        self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)

    def listen(self, num_clients:int) -> None:
        '''Binds the server and starts listenting for the specified number of clients.
        
        Parameters
        ----------
        num_clients : int
            The number of clients to listen for
        '''
        self.socket.bind((self.IP, self.PORT))
        self.socket.listen(num_clients)
        if self.verbose:
            print('~~~ Server has started ~~~')
            print(f"IP: {self.IP}")
            print(f"PORT: {self.PORT}")
            print(f"MAX-QUEUE: {num_clients}")
            print(f"BUFFER-SIZE: {self.BUFFER_SIZE} ")
            print(f"ENCODING: {self.encoding}")
            print(f"ENCRYPTION: {self.encryption} bytes")
            print('~~~~~~~ Listening ~~~~~~~')


    def accept(self) -> int:
        '''Accepts a new connection and returns an ID of accepted client.'''
        sock, addr = self.socket.accept()
        client_id = len(self.clients) + 1

        # Proceed to swap encryption keys between server and client
        if self.encryption > 0:
            server_private_key = RSA.generate(self.encryption)
            server_public_key = server_private_key.publickey()

            sock.send(
                header_the_message(
                    server_public_key.export_key().decode(), 
                    self.HEADER_SIZE
                )
                .encode(self.encoding)
            )

            client_public_key = RSA.import_key(
                recv(sock, self.HEADER_SIZE, self.BUFFER_SIZE, self.encoding)
            )

            self.clients[client_id] = [sock, client_public_key, server_private_key]

        else:
            self.clients[client_id] = [sock]

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

    def get_client_ip(self, client_id) -> str:
        '''Returns a client ip address by his id in the `clients` dictionary

        Parameters
        ----------
        client_id : int
            Client id in the dictionary

        '''
        return self.clients[client_id][0].getpeername()[0]

    def send(self, message:str, client_id:int) -> None:
        '''Sends a message to a client by the specified client ID.
        
        Parameters
        ----------
        message : str
            Message that will be sent to the client
        client_id : int
            Client id in the dictionary
        '''

        if self.encryption > 0:

            encryptor           = PKCS1_OAEP.new(key=self.clients[client_id][1])
            encrypted_message   = encryptor.encrypt(message.encode(self.encoding))

            self.clients[client_id][0].send(
                header_the_message(encrypted_message.decode(), self.HEADER_SIZE)
                .encode(self.encoding)
            )    

        else:
            self.clients[client_id][0].send(
                header_the_message(message, self.HEADER_SIZE)
                .encode(self.encoding)
            )

    def send_all(self, message: str, ignore_client_id: int=None) -> None:
        '''Sends specified message to all clients.

        If the argument `ignore_client_id` is passed in, specified client will be ignored when sending the message.

        Parameters
        ----------
        message : str
            Message that will be sent to all clients
        ignore_client_id : int
            Client that will be ignored when sending the message
        '''

        for client in [self.clients[i] for i in self.clients]:

            client_socket = client[0]

            if self.encryption > 0:

                encryptor           = PKCS1_OAEP.new(key=client[1])
                encrypted_message   = encryptor.encrypt(message.encode())
                broadcast           = header_the_message(encrypted_message, self.HEADER_SIZE).encode(self.encoding)

            else:
                broadcast = header_the_message(message, self.HEADER_SIZE).encode(self.encoding)


            if ignore_client_id:
                if client_socket != self.clients[ignore_client_id][0]:
                    client_socket.send(broadcast)
            else:
                client_socket.send(broadcast)

    def recv(self, client_id:int) -> str:
        '''Returns message received from the client
        
        Parameters
        ----------
        client_id : str
            Client id in the dictionary
        '''

        if self.encryption > 0:
            
            decryptor = PKCS1_OAEP.new(key=self.clients[client_id][2])

            return recv(
                self.clients[client_id][0], 
                self.HEADER_SIZE, 
                self.BUFFER_SIZE, 
                decryptor=decryptor
            )

        else:
            return recv(self.clients[client_id][0], self.HEADER_SIZE, self.BUFFER_SIZE)

    def close(self) -> None:
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
    encryption : bool
        Sets the encryption level to twice the buffer size, 0 if False (default is True)
    '''

    def __init__(self, IP: str='127.0.0.1', PORT: int=5000, BUFFER_SIZE: int=1024, HEADER_SIZE: int=50, encoding: str='utf-8', verbose: bool=False, encryption: bool=True) -> None:
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
        verbose : bool
            Displays client information (default is False)
        encryption : bool
            Sets the encryption level to twice the buffer size, 0 if False (default is True)
        '''
        self.IP = IP
        self.PORT = PORT
        self.BUFFER_SIZE = BUFFER_SIZE
        self.HEADER_SIZE = HEADER_SIZE

        if encryption:
            self.encryption = BUFFER_SIZE * 2
        else:
            self.encryption = 0

        # Encription
        self.encoding = encoding
        self.server_public_key = None
        self.client_private_key = None

        self.encryptor = None
        self.decryptor = None
    
        self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)

        if verbose:
            print('~~~ Client information ~~~')
            print(f"IP: {self.IP} ")
            print(f"PORT: {self.PORT}")
            print(f"BUFFER-SIZE: {self.BUFFER_SIZE}")
            print(f"ENCODING: {self.encoding}")
            print(f"ENCRYPTION: {self.encryption} bytes")
            print('~~~~~~~ Connecting ~~~~~~~')

    def connect(self) -> None:
        '''Connects to the specified earlier IP and PORT'''
        self.socket.connect((self.IP, self.PORT))

        if self.encryption > 0:

            self.client_private_key = RSA.generate(self.encryption)
            client_public_key = self.client_private_key.publickey()

            self.server_public_key = RSA.import_key(
                recv(self.socket, self.HEADER_SIZE, self.BUFFER_SIZE, self.encoding)
            )

            self.socket.send( 
                header_the_message(
                    client_public_key.export_key().decode(), self.HEADER_SIZE
                )
                .encode(self.encoding)
            )

            self.encryptor = PKCS1_OAEP.new(key=self.server_public_key)
            self.decryptor = PKCS1_OAEP.new(key=self.client_private_key)

    def send(self, message:str) -> None:
        ''' Sends the specified message to the server.

        Parameters
        ----------
        message : str
            Message that will be sent to the server //needs to be in decoded form when passing
            The message is also getting encrypted if encryption is on
        '''

        if self.encryption > 0:
            #sliced_message = split_message(message, self.BUFFER_SIZE)
            message = self.encryptor.encrypt(message.encode())

        self.socket.send( 
            header_the_message(message, self.HEADER_SIZE).encode(self.encoding)
            )

    def close(self) -> None:
        '''Closes the client socket'''
        self.socket.close()

    def recv(self) -> str:
        '''Receives full message'''

        return recv(
            self.socket, 
            self.HEADER_SIZE, 
            self.BUFFER_SIZE,
            decryptor=self.decryptor
        )