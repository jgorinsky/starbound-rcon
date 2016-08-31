import logging
import socket
import struct

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

SERVER = ('', 21026)
PASS = ''

CLIENT_ID = 42

SERVERDATA_AUTH = 3
SERVERDATA_EXECCOMMAND = 2
SERVERDATA_RESPONSE_VALUE = 0

FMT = '<iii{0}ss'

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect(SERVER)
    # Start auth
    s.send(make_buf(SERVERDATA_AUTH, PASS))
    # Receive empty SERVERDATA_RESPONSE_VALUE
    receive_packet(s)
    # Receive SERVERDATA_AUTH
    receive_packet(s)
    # Send command
    s.send(make_buf(SERVERDATA_EXECCOMMAND, 'help'))
    # Receive command response
    receive_packet(s)

    s.close()


def receive_packet(s):
    length = unpack_length(s.recv(4))
    logger.debug('receiving packet of length %s', length)
    packet = unpack(s.recv(length), length - 9)
    logger.debug('receieved %s', packet)
    return packet


def make_buf(type, body):
    length = len(body)
    return struct.pack(FMT.format(length + 1), 10 + length, CLIENT_ID, type, bytes(body, 'ascii'), b'')

def unpack_length(buf):
    return struct.unpack('<i', buf)[0]

def unpack(buf, body_length):
    logger.debug(buf)
    id, type, body, nil = struct.unpack('<ii{0}ss'.format(body_length), buf)
    logger.debug('%s %s %s', id, type, body)
    return { 'id': id, 'type': type, 'body': body[0:-1].decode('ascii') }

if __name__ == '__main__':
    main()
