import logging
import socket
import struct
import argparse

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

DEFAULT_CLIENT_ID = 42

SERVERDATA_AUTH = 3
SERVERDATA_EXECCOMMAND = 2
SERVERDATA_AUTH_RESPONSE = 2
SERVERDATA_RESPONSE_VALUE = 0

PACKET_FMT = '<iii{0}ss'

class Packet:
    def __init__(self, id, type, body):
        self.id = id
        self.type = type
        self.body = body
    def __str__(self):
        return '<ID: %s, Type: %s, Body: %s>' % (self.id, self.type, self.body)

class Rcon:
    def __init__(self, server, port, password, client_id=DEFAULT_CLIENT_ID):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((server, port))
        self.client_id = client_id
        authenticate(self.sock, password, client_id)

    def send(self, command):
        packet = send(self.sock, self.client_id, command)
        return packet.body

    def close(self):
        self.sock.close()

def send(sock, client_id, command):
    sock.send(make_buf(SERVERDATA_EXECCOMMAND, client_id, command))
    packet = receive_packet(sock)
    assert packet.type == SERVERDATA_RESPONSE_VALUE
    assert packet.id == client_id
    return packet

def authenticate(sock, password, client_id):
    # Start auth
    sock.send(make_buf(SERVERDATA_AUTH, client_id, password))
    # Receive empty SERVERDATA_RESPONSE_VALUE
    empty_pack = receive_packet(sock)

    if empty_pack.id == -1:
        raise Exception('Authentication error')
    assert empty_pack.type == SERVERDATA_RESPONSE_VALUE
    assert empty_pack.body == ''

    # Receive SERVERDATA_AUTH
    auth_pack = receive_packet(sock)
    assert auth_pack.type == SERVERDATA_AUTH_RESPONSE
    assert auth_pack.id == client_id

def receive_packet(s):
    length = unpack_length(s.recv(4))
    logger.debug('receiving packet of length %s', length)
    packet = unpack(s.recv(length), length - 9)
    logger.debug('receieved %s', packet)
    return packet


def make_buf(type, client_id, body):
    length = len(body)
    return struct.pack(PACKET_FMT.format(length + 1), 10 + length, client_id, type, body.encode('ascii'), b'')

def unpack_length(buf):
    return struct.unpack('<i', buf)[0]

def unpack(buf, body_length):
    logger.debug(buf)
    id, type, body, nil = struct.unpack('<ii{0}ss'.format(body_length), buf)
    return Packet(id, type, body[0:-1].decode('ascii'))

def parseOpts():
    parser = argparse.ArgumentParser(description='Send a command to a Starbound RCON server')
    parser.add_argument('--server', '-s', metavar='server', help='RCON server url')
    parser.add_argument('--port', '-P', metavar='port', type=int, default=21026, help='RCON server port')
    parser.add_argument('--password', '-p', metavar='password', help='RCON server password')
    parser.add_argument('command', help='command to send to the server')
    return vars(parser.parse_args())

def main():
    opts = parseOpts()
    rcon = Rcon(opts['server'], opts['port'], opts['password'])
    print(rcon.send(opts['command']))
    rcon.close()
