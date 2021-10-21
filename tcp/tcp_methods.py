from Crypto.Cipher import PKCS1_OAEP
import ast

def caclulate_space(HEADER_SIZE:int, message_length:int) -> str:
    return ' ' * (HEADER_SIZE - len(str(message_length)))


def split_message(message: str, split_size: int) -> list:
    return [message[i:i+split_size] for i in range(0, len(message), split_size)]
    


def header_the_message(message:str, HEADER_SIZE:int = 50) -> str:
    '''Makes header with information about the message

    Parameters
    ----------
    message : str
        Message that will be embeded with a header
    HEADER_SIZE : int
        Default size of a header message containing information that will come before any message is sent (default is 50)
    '''

    message_length = len(str(message))
    space_leftout = caclulate_space(HEADER_SIZE, message_length)

    return f"{message_length}{space_leftout}{message}"



def recv(client, HEADER_SIZE: int=50, BUFFER_SIZE: int=1024, encoding: str='utf-8', decryptor=None) -> str:
    '''Decodes the header and receives the full message that was sent.
    
    Will return None if the connection is closed.

    Parameters
    ----------
    client : socket.socket
        Client socket that the information will be received from.
    HEADER_SIZE : int
        Default size of a header message containing information that will come before any message is sent (default is 50)
    BUFFER_SIZE : int
            Default buffer size that the server will use when i/o requests (default is 1024)
    encoding : str
        Charset that all the messages will be encoded in (default is utf-8)
    decryptor
        Decryps the message if the decryptor is provided
    '''

    try:

        header_message = client.recv(HEADER_SIZE)

        incoming_message_length = int(header_message.decode(encoding))
        final_message = ""

        if incoming_message_length < BUFFER_SIZE:
            final_message += client.recv(incoming_message_length).decode(encoding)

        else:
            times_to_recv_buffer = (incoming_message_length // BUFFER_SIZE)

            for i in range(times_to_recv_buffer):
                final_message += client.recv(BUFFER_SIZE).decode(encoding)
            
            last_message_length = incoming_message_length - BUFFER_SIZE * (times_to_recv_buffer)
            final_message += client.recv(last_message_length).decode(encoding)

        if decryptor:
            final_message = ast.literal_eval(final_message)
            final_message = decryptor.decrypt(final_message).decode(encoding)

        return final_message

    except ConnectionResetError as e:
        return None
