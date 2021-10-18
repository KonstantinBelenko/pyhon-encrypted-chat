'''
This package allows simpler and faster
use of socket library for TCP/IP protocol
communication and encryption purposes 
'''

import socket as s
from .tcp_classes import Client, Server

__version__ = '0.0.1'
__author__ = 'Konstantin Belenko'

__all__ = ['socket', '__version__', '__author__']

