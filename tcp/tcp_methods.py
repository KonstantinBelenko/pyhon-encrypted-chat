def header_the_message(message:str, HEADER_SIZE:int = 50) -> str:
    '''Makes header with information about the message

    ...

    Format
    ------
    h{message_length}>{space_leftout}{message}

    Parameters
    ----------
    message : str
        Message that will be embeded with a header
    HEADER_SIZE : int
        Default size of a header message containing information that will come before any message is sent (default is 50)
    '''

    # This considers the space marking symbols ['h', '>'] take in the header  
    HEADER_SIZE -= 2
    message_length = len(message)
    space_leftout = ' ' * (HEADER_SIZE - len(str(message_length)))

    return f"h{message_length}>{space_leftout}{message}"

def recv(client, HEADER_SIZE:int = 50, BUFFER_SIZE:int = 1024, encoding:str = 'utf-8') -> str:
    '''Decodes the header and receives the full message that was sent.
    
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
    '''
    header = client.recv(HEADER_SIZE).decode(encoding)
    message_length = int(header[1:header.find('>')])
    final_message = ''

    if message_length < BUFFER_SIZE:
        final_message += client.recv(message_length).decode(encoding)
    else:
        times_to_loop = times_to_loop

        # Repeat until everything has been received
        for i in range(times_to_loop):
            final_message += client.recv(BUFFER_SIZE).decode(encoding)
        
        last_message_length = message_length - BUFFER_SIZE * (times_to_loop)
        final_message += client.recv(last_message_length).decode(encoding)

    return final_message
